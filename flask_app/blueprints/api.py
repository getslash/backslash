from contextlib import contextmanager
import datetime
import functools
import logbook

import requests
from flask import abort, Blueprint, request, g
from flask.ext.simple_api import SimpleAPI
from flask.ext.simple_api import error_abort
from flask.ext.security import current_user

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from .. import activity
from .. import stats
from .. import models
from ..models import db, Error, Session, SessionMetadata, Test, TestMetadata, Comment, User, Role, Warning, RelatedEntity, TestVariation
from ..utils import get_current_time, statuses
from ..utils.api_utils import API_SUCCESS, auto_render, requires_login_or_runtoken, requires_login, requires_role
from ..utils.rendering import render_api_object
from ..utils.subjects import get_or_create_subject_instance
from ..utils.test_information import get_or_create_test_information_id
from ..utils.users import get_user_id_by_email, has_role

blueprint = Blueprint('api', __name__, url_prefix='/api')

api = SimpleAPI(blueprint)

NoneType = type(None)


def API(func=None, require_real_login=False, generates_activity=True):
    if func is None:
        return functools.partial(API, require_real_login=require_real_login, generates_activity=generates_activity)

    returned = auto_render(func)

    if generates_activity:
        returned = activity.updates_last_active(returned)

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
                         user_email: str=None,
                         keepalive_interval: (NoneType, int)=None,
                         subjects: (list, NoneType)=None,
                         ):
    if hostname is None:
        hostname = request.remote_addr

    # fix user identification
    if user_email is not None and user_email != g.token_user.email:
        if not has_role(g.token_user.id, 'proxy'):
            error_abort('User is not authorized to run tests on others behalf', code=requests.codes.forbidden)
        real_user_id = g.token_user.id
        user_id = get_user_id_by_email(user_email)
    else:
        user_id = g.token_user.id
        real_user_id = None

    returned = Session(
        hostname=hostname,
        total_num_tests=total_num_tests,
        user_id=user_id,
        real_user_id=real_user_id,
        status=statuses.RUNNING,
        logical_id=logical_id,
        keepalive_interval=keepalive_interval,
        next_keepalive=None if keepalive_interval is None else get_current_time() + keepalive_interval,
    )

    if subjects:
        for subject_data in subjects:
            subject_name = subject_data.get('name', None)
            if subject_name is None:
                error_abort('Missing subject name')
            subject = get_or_create_subject_instance(
                name=subject_name,
                product=subject_data.get('product', None),
                version=subject_data.get('version', None),
                revision=subject_data.get('revision', None))
            returned.subject_instances.append(subject)

    if metadata is not None:
        for key, value in metadata.items():
            returned.metadata_items.append(SessionMetadata(session=returned, key=key, metadata_item=value))

    db.session.add(returned)
    db.session.commit()
    return returned

@API
def send_keepalive(session_id: int):
    s = Session.query.get_or_404(session_id)
    s.next_keepalive = get_current_time() + s.keepalive_interval
    db.session.add(s)
    db.session.commit()

@API
def add_subject(session_id: int, name: str, product: (str, NoneType)=None, version: (str, NoneType)=None, revision: (str, NoneType)=None):
    session = Session.query.get_or_404(session_id)
    subject = get_or_create_subject_instance(
        name=name,
        product=product,
        version=version,
        revision=revision)
    session.subject_instances.append(subject)
    db.session.add(session)
    db.session.commit()


@API
def add_related_entity(type: str, name: str, test_id: int=None, session_id: int=None):
    if not ((test_id is not None) ^ (session_id is not None)):
        error_abort('Either test_id or session_id required')

    db.session.add(RelatedEntity(
        test_id = test_id,
        session_id = session_id,
        type=type,
        name=name
        ))
    db.session.commit()



@API
def report_session_end(id: int, duration: (int, NoneType)=None):
    try:
        session = Session.query.filter(Session.id == id).one()
    except NoResultFound:
        error_abort('Session not found', code=requests.codes.not_found)

    if session.status not in (statuses.RUNNING, statuses.INTERRUPTED):
        error_abort('Session is not running', code=requests.codes.conflict)

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
    db.session.commit()


@API
def report_test_start(
        session_id: int,
        name: str,
        file_name: (str, NoneType)=None,
        class_name: (str, NoneType)=None,
        test_logical_id: str=None,
        scm: (str, NoneType)=None,
        file_hash: (str, NoneType)=None,
        scm_revision: (str, NoneType)=None,
        scm_dirty: bool=False,
        is_interactive: bool=False,
        variation: (dict, NoneType)=None,
):
    session = Session.query.get(session_id)
    if session is None:
        abort(requests.codes.not_found)
    if session.end_time is not None:
        error_abort('Session already ended', code=requests.codes.conflict)
    test_info_id = get_or_create_test_information_id(
        file_name=file_name, name=name, class_name=class_name)
    if is_interactive:
        session.total_num_tests = Session.total_num_tests + 1
        db.session.add(session)
    returned = Test(
        session_id=session.id,
        logical_id=test_logical_id,
        test_info_id=test_info_id,
        status=statuses.RUNNING,
        scm_dirty=scm_dirty,
        scm_revision=scm_revision,
        scm=scm,
        is_interactive=is_interactive,
        file_hash=file_hash,
    )
    if variation is not None:
        returned.test_variation = TestVariation(variation=variation)
    db.session.add(returned)
    db.session.commit()
    return returned


@API
def report_test_end(id: int, duration: (float, int)=None):
    test = Test.query.get(id)
    if test is None:
        abort(requests.codes.not_found)

    if test.end_time is not None:
        # we have a test, but it already ended
        error_abort('Test already ended', code=requests.codes.conflict)

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
    db.session.commit()


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
def report_test_skipped(id: int, reason: (str, NoneType)=None):
    _update_running_test_status(
        id, statuses.SKIPPED, ignore_conflict=True,
        additional_updates={'skip_reason': reason})
    db.session.commit()


@API
def report_test_interrupted(id: int):
    _update_running_test_status(id, statuses.INTERRUPTED)
    db.session.commit()

@API(require_real_login=True)
@requires_role('moderator')
def toggle_archived(session_id: int):
    returned = _toggle_session_attribute(session_id, 'archived', activity.ACTION_ARCHIVED, activity.ACTION_UNARCHIVED)
    db.session.commit()
    return returned

@API(require_real_login=True)
def toggle_investigated(session_id: int):
    returned = _toggle_session_attribute(session_id, 'investigated', activity.ACTION_INVESTIGATED, activity.ACTION_UNINVESTIGATED)
    db.session.commit()

def _toggle_session_attribute(session_id, attr, on_action, off_action):
    session = Session.query.get_or_404(session_id)
    new_value = not getattr(session, attr)
    setattr(session, attr, new_value)
    db.session.add(session)
    activity.register_user_activity(on_action if new_value else off_action, session_id=session_id)



def _update_running_test_status(test_id, status, ignore_conflict=False, additional_updates=None):
    logbook.debug('marking test {} as {}', test_id, status)
    updates = {'status': status}
    if additional_updates:
        updates.update(additional_updates)

    if not Test.query.filter(Test.id == test_id, Test.status == statuses.RUNNING).update(updates):
        if Test.query.filter(Test.id == test_id).count():
            # we have a test, but it already ended
            if not ignore_conflict:
                error_abort('Test already ended', requests.codes.conflict)
        else:
            abort(requests.codes.not_found)

@API
def set_metadata(entity_type: str, entity_id: int, key: str, value: object):
    _set_metadata_dict(entity_type=entity_type, entity_id=entity_id, metadata={key: value})


@API
def set_metadata_dict(entity_type: str, entity_id: int, metadata: dict):
    _set_metadata_dict(entity_type=entity_type, entity_id=entity_id, metadata=metadata)


def _set_metadata_dict(*, entity_type, entity_id, metadata):
    model = _get_metadata_model(entity_type)
    for key, value in metadata.items():
        db.session.add(model(key=key, metadata_item=value, **{'{}_id'.format(entity_type): entity_id}))
    try:
        db.session.commit()
    except IntegrityError:
        abort(requests.codes.not_found)



@API(generates_activity=True)
def get_metadata(entity_type: str, entity_id: (int, str)):
    query = _get_metadata_query(entity_type=entity_type, entity_id=entity_id)
    return {obj.key: obj.metadata_item for obj in query}


def _get_metadata_query(*, entity_type, entity_id):
    model = _get_metadata_model(entity_type)
    if entity_type == 'session':
        related = Session
    elif entity_type == 'test':
        related = Test
    else:
        error_abort('Invalid entity type', requests.codes.bad_request)
    if isinstance(entity_id, int):
        return model.query.filter_by(**{'{}_id'.format(entity_type): entity_id})
    return model.query.join(related).filter(related.logical_id == entity_id)


def _get_metadata_model(entity_type):
    if entity_type == 'session':
        return SessionMetadata

    if entity_type == 'test':
        return TestMetadata

    error_abort('Unknown entity type')


@API
def add_test_metadata(id: int, metadata: dict):
    try:
        test = Test.query.filter(Test.id == id).one()
        test.metadata_objects.append(TestMetadata(metadata_item=metadata))
    except NoResultFound:
        abort(requests.codes.not_found)
    db.session.commit()


@API
def add_session_metadata(id: int, metadata: dict):
    try:
        session = Session.query.filter(Session.id == id).one()
        session.metadata_objects.append(
            SessionMetadata(metadata_item=metadata))
    except NoResultFound:
        abort(requests.codes.not_found)
    db.session.commit()


@API
def add_error(message: str, exception_type: (str, NoneType)=None, traceback: (list, NoneType)=None, timestamp: (float, int)=None, test_id: int=None, session_id: int=None, is_failure: bool=False):
    if not ((test_id is not None) ^ (session_id is not None)):
        error_abort('Either test_id or session_id required')

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
                                traceback=_normalize_traceback(traceback),
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
    db.session.commit()

def _normalize_traceback(traceback_json):
    if traceback_json:
        for frame in traceback_json:
            code_string = frame['code_string']
            if code_string:
                code_string = code_string.splitlines()[-1]
            frame['code_string'] = code_string
    return traceback_json

@API
def add_warning(message: str, filename: str=None, lineno: int=None, test_id: int=None, session_id: int=None, timestamp: (int, float)=None):
    if not ((test_id is not None) ^ (session_id is not None)):
        error_abort('Either session_id or test_id required')
    if session_id is not None:
        obj = Session.query.get_or_404(session_id)
    else:
        obj = Test.query.get_or_404(test_id)
    if timestamp is None:
        timestamp = get_current_time()
    db.session.add(
        Warning(message=message, timestamp=timestamp, filename=filename, lineno=lineno, test_id=test_id, session_id=session_id))
    obj.num_warnings = type(obj).num_warnings + 1
    if session_id is None:
        obj.session.num_test_warnings = Session.num_test_warnings + 1
        db.session.add(obj.session)

    db.session.add(obj)
    db.session.commit()



@API(require_real_login=True)
def post_comment(comment: str, session_id: int=None, test_id: int=None):
    if not (session_id is not None) ^ (test_id is not None):
        error_abort('Either session_id or test_id required')

    if session_id is not None:
        obj = db.session.query(Session).get(session_id)
    else:
        obj = db.session.query(Test).get(test_id)

    returned = Comment(user_id=current_user.id, comment=comment)
    obj.comments.append(returned)
    db.session.commit()
    return returned



@API(require_real_login=True)
def delete_comment(comment_id: int):

    comment = Comment.query.get_or_404(comment_id)

    if not comment.can()['delete']:
        abort(requests.codes.forbidden)

    comment.deleted = True
    comment.comment = ''

    db.session.add(comment)
    db.session.commit()

@API(require_real_login=True)
@requires_role('admin')
def toggle_user_role(user_id: int, role: str):
    user = User.query.get_or_404(user_id)
    role_obj = Role.query.filter_by(name=role).first_or_404()

    if role_obj in user.roles:
        user.roles.remove(role_obj)
    else:
        user.roles.append(role_obj)
    db.session.commit()

@API(require_real_login=True)
def get_user_run_tokens(user_id: int):
    if not has_role(current_user, 'admin') and current_user.id != user_id:
        abort(requests.codes.forbidden)
    return [t.token for t in User.query.get_or_404(user_id).run_tokens]

@API(require_real_login=True)
@requires_role('admin')
def get_admin_stats():
    returned = {}
    history = returned['history'] = []

    for s in models.Stat.query.order_by('timestamp asc').all():
        item = {'timestamp': s.timestamp}
        item.update({name: getattr(s, 'stat_' + name) for name in stats.iter_stat_names()})
        history.append(item)
    return returned
