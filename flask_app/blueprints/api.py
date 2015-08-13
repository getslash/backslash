from contextlib import contextmanager
import datetime
import functools
import logbook

import requests
from flask import abort, Blueprint, request, g
from flask.ext.simple_api import SimpleAPI
from flask.ext.security import current_user

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from .. import activity
from ..models import db, Error, Session, SessionMetadata, Test, TestMetadata, Comment
from ..utils import get_current_time, statuses
from ..utils.api_utils import API_SUCCESS, auto_commit, auto_render, requires_login_or_runtoken, requires_login
from ..utils.subjects import get_or_create_subject_instance
from ..utils.test_information import get_or_create_test_information_id

blueprint = Blueprint('api', __name__, url_prefix='/api')

api = SimpleAPI(blueprint)

NoneType = type(None)


def API(func=None, require_real_login=False):
    if func is None:
        return functools.partial(API, require_real_login=require_real_login)

    returned = auto_render(auto_commit(func))
    if require_real_login:
        returned = requires_login(returned)
    else:
        returned = requires_login_or_runtoken(returned)
    return api.include(returned)

##########################################################################


@API
def report_session_start(logical_id: str=None,
                         hostname: str=None,
                         total_num_tests: int=None,
                         metadata: dict=None,
                         ):
    if hostname is None:
        hostname = request.remote_addr
    returned = Session(
        hostname=hostname,
        total_num_tests=total_num_tests,
        user_id=g.token_user.id,
        status=statuses.RUNNING,
        logical_id=logical_id,
    )
    if metadata is not None:
        for key, value in metadata.items():
            db.session.add(
                SessionMetadata(session=returned, key=key, metadata_item=value))
    return returned


@API
def add_subject(session_id: int, name: str, product: (str, NoneType)=None, version: (str, NoneType)=None, revision: (str, NoneType)=None):
    session = Session.query.get_or_404(session_id)
    subject = get_or_create_subject_instance(
        name=name,
        product=product,
        version=version,
        revision=revision)
    db.session.add(subject)
    session.subject_instances.append(subject)
    db.session.add(session)


@API
def report_session_end(id: int, duration: int=None):
    try:
        session = Session.query.filter(Session.id == id).one()
    except NoResultFound:
        abort(requests.codes.not_found)

    if session.status not in (statuses.RUNNING, statuses.INTERRUPTED):
        abort(requests.codes.conflict)

    session.end_time = get_current_time(
    ) if duration is None else session.start_time + duration
    # TODO: handle interrupted sessions
    if session.num_error_tests or session.num_errors:
        session.status = statuses.ERROR
    elif session.num_failed_tests or session.num_failures:
        session.status = statuses.FAILURE
    else:
        session.status = statuses.SUCCESS
    db.session.add(session)


@API
def report_test_start(session_id: int, name: str, file_name: (str, NoneType)=None, class_name: (str, NoneType)=None, test_logical_id: str=None):
    session = Session.query.get(session_id)
    if session is None:
        abort(requests.codes.not_found)
    if session.end_time is not None:
        abort(requests.codes.conflict)
    test_info_id = get_or_create_test_information_id(
        file_name=file_name, name=name, class_name=class_name)
    return Test(session_id=session.id, logical_id=test_logical_id, test_info_id=test_info_id, status=statuses.RUNNING)


@API
def report_test_end(id: int, duration: (float, int)=None):
    test = Test.query.get(id)
    if test is None:
        abort(requests.codes.not_found)

    if test.end_time is not None:
        # we have a test, but it already ended
        abort(requests.codes.conflict)

    with updating_session_counters(test):
        test.end_time = get_current_time() if duration is None else Test.start_time + \
            duration
        if test.num_errors:
            test.status = statuses.ERROR
        elif test.num_failures:
            test.status = statuses.FAILURE
        elif not test.interrupted and not test.skipped:
            test.status = statuses.SUCCESS

    db.session.add(test)


@contextmanager
def updating_session_counters(test):
    was_running = test.end_time is None
    was_success = not test.errored and not test.failed
    yield
    session_update = {}
    is_ended = test.end_time is not None
    if is_ended:
        if was_running:
            session_update[
                'num_finished_tests'] = Session.num_finished_tests + 1

        if test.errored and (was_running or was_success):
            session_update['num_error_tests'] = Session.num_error_tests + 1

        if test.failed and (was_running or was_success):
            session_update['num_failed_tests'] = Session.num_failed_tests + 1

        if test.skipped and was_running:
            session_update['num_skipped_tests'] = Session.num_skipped_tests + 1

    if session_update:
        Session.query.filter(
            Session.id == test.session_id).update(session_update)


@API
def report_test_skipped(id: int):
    _update_running_test_status(id, statuses.SKIPPED, ignore_conflict=True)


@API
def report_test_interrupted(id: int):
    _update_running_test_status(id, statuses.INTERRUPTED)

@API(require_real_login=True)
def toggle_archived(session_id: int):
        return _toggle_session_attribute(session_id, 'archived', activity.ACTION_ARCHIVED, activity.ACTION_UNARCHIVED)

@API(require_real_login=True)
def toggle_investigated(session_id: int):
    return _toggle_session_attribute(session_id, 'investigated', activity.ACTION_INVESTIGATED, activity.ACTION_UNINVESTIGATED)

def _toggle_session_attribute(session_id, attr, on_action, off_action):
    session = Session.query.get_or_404(session_id)
    new_value = not getattr(session, attr)
    setattr(session, attr, new_value)
    db.session.add(session)
    activity.register_user_activity(on_action if new_value else off_action, session_id=session_id)



def _update_running_test_status(test_id, status, ignore_conflict=False):
    logbook.debug('marking test {} as {}', test_id, status)

    if not Test.query.filter(Test.id == test_id, Test.status == statuses.RUNNING).update({'status': status}):
        if Test.query.filter(Test.id == test_id).count():
            # we have a test, but it already ended
            if not ignore_conflict:
                abort(requests.codes.conflict)
        else:
            abort(requests.codes.not_found)

@API
def set_metadata(entity_type: str, entity_id: int, key: str, value: object):
    model, kwargs = _get_metadata_model(entity_type, entity_id)
    db.session.add(model(key=key, metadata_item=value, **kwargs))
    try:
        db.session.commit()
    except IntegrityError:
        abort(requests.codes.not_found)


@API
def get_metadata(entity_type: str, entity_id: int):
    model, kwargs = _get_metadata_model(entity_type, entity_id)
    return {obj.key: obj.metadata_item
            for obj in model.query.filter_by(**kwargs)}


def _get_metadata_model(entity_type, entity_id):
    if entity_type == 'session':
        return SessionMetadata, {'session_id': entity_id}

    if entity_type == 'test':
        return TestMetadata, {'test_id': entity_id}

    abort(requests.codes.bad_request)


@API
def add_test_metadata(id: int, metadata: dict):
    try:
        test = Test.query.filter(Test.id == id).one()
        test.metadata_objects.append(TestMetadata(metadata_item=metadata))
    except NoResultFound:
        abort(requests.codes.not_found)


@API
def add_session_metadata(id: int, metadata: dict):
    try:
        session = Session.query.filter(Session.id == id).one()
        session.metadata_objects.append(
            SessionMetadata(metadata_item=metadata))
    except NoResultFound:
        abort(requests.codes.not_found)


@API
def add_error(message: str, exception_type: str=None, traceback: list=None, timestamp: (float, int)=None, test_id: int=None, session_id: int=None, is_failure: bool=False):
    if not ((test_id is not None) ^ (session_id is not None)):
        abort(requests.codes.bad_request)

    if timestamp is None:
        timestamp = get_current_time()
    if test_id is not None:
        cls = Test
        object_id = test_id
    else:
        cls = Session
        object_id = session_id

    try:
        obj = cls.query.filter(cls.id == object_id).one()
        increment_field = cls.num_failures if is_failure else cls.num_errors
        cls.query.filter(cls.id == object_id).update(
            {increment_field: increment_field + 1})
        obj.errors.append(Error(message=message,
                                exception_type=exception_type,
                                traceback=traceback,
                                is_failure=is_failure,
                                timestamp=timestamp))
        if obj.end_time is not None:
            if cls is Test:
                if is_failure and obj.status not in (statuses.FAILURE, statuses.ERROR):
                    obj.status = statuses.FAILURE
                    obj.session.num_failed_tests = Session.num_failed_tests + 1
                elif not is_failure and obj.status != statuses.ERROR:
                    if obj.status == statuses.FAILURE:
                        db.session.num_failed_tests = Session.num_failed_tests - 1
                    obj.status = statuses.ERROR
                    obj.session.num_error_tests = Session.num_error_tests + 1
        db.session.add(obj)

    except NoResultFound:
        abort(requests.codes.not_found)


@API(require_real_login=True)
def post_comment(comment: str, session_id: int=None, test_id: int=None):
    if not (session_id is not None) ^ (test_id is not None):
        abort(requests.codes.bad_request)

    if session_id is not None:
        obj = db.session.query(Session).get(session_id)
    else:
        obj = db.session.query(Test).get(test_id)

    returned = Comment(user_id=current_user.id, comment=comment)
    obj.comments.append(returned)
    db.session.commit()
    return {'id': returned.id}



@API(require_real_login=True)
def delete_comment(comment_id: int):

    comment = Comment.query.get_or_404(comment_id)

    if not comment.can()['delete']:
        abort(requests.codes.forbidden)

    comment.deleted = True
    comment.comment = ''

    db.session.add(comment)
