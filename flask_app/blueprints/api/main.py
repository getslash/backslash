from contextlib import contextmanager
import logbook

import requests
from flask import abort, current_app
from flask_simple_api import error_abort
from flask_security import current_user

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import DataError

from .blueprint import API
from ... import metrics
from ...models import db, Session, Test, Comment, User, Role, Warning, Entity, TestVariation, TestMetadata
from ...utils import get_current_time, statuses
from ...utils.api_utils import requires_role
from ...utils.subjects import get_or_create_subject_instance
from ...utils.test_information import get_or_create_test_information_id
from ...utils.users import has_role
from ...utils.json import sanitize_json


##########################################################################

from . import setup # pylint: disable=unused-import
from . import sessions # pylint: disable=unused-import
from . import metadata # pylint: disable=unused-import
from . import preferences # pylint: disable=unused-import
from . import errors # pylint: disable=unused-import
from . import labels # pylint: disable=unused-import
from . import quick_search # pylint: disable=unused-import
from .blueprint import blueprint # pylint: disable=unused-import


NoneType = type(None)


@API
def add_subject(session_id: int, name: str, product: (str, NoneType)=None, version: (str, NoneType)=None, revision: (str, NoneType)=None):
    session = Session.query.get_or_404(session_id)
    subject = get_or_create_subject_instance(
        name=name,
        product=product,
        version=version,
        revision=revision)
    subject.subject.last_activity = get_current_time()
    session.subject_instances.append(subject)
    db.session.add(session)
    db.session.commit()


@API
def add_related_entity(type: str, name: str, test_id: int=None, session_id: int=None):
    #pylint: disable=superfluous-parens
    if not ((test_id is not None) ^ (session_id is not None)):
        error_abort('Either test_id or session_id required')

    if session_id is not None:
        obj = Session.query.get_or_404(session_id)
    else:
        obj = Test.query.get_or_404(test_id)

    db.session.execute(insert(Entity).values(name=name, type=type).on_conflict_do_nothing())
    db.session.commit()

    entity = Entity.query.filter_by(name=name, type=type).one()

    obj.related_entities.append(entity)
    db.session.commit()

def _validate_session(session_id):
    session = Session.query.get(session_id)
    if session is None:
        abort(requests.codes.not_found)
    if session.end_time is not None:
        error_abort('Session already ended', code=requests.codes.conflict)
    return session

@API
def append_upcoming_tests(tests: list, session_id: int):
    session = _validate_session(session_id)
    new_tests = []
    for test in tests:
        test_info_id = get_or_create_test_information_id(file_name=test['file_name'], name=test['name'], class_name=test['class_name'])
        new_test = Test(
            session_id=session.id,
            logical_id=test['test_logical_id'],
            test_info_id=test_info_id,
            status=statuses.PLANNED
        )
        if 'variation' in test:
            new_test.test_variation = TestVariation(variation=sanitize_json(test['variation']))
        new_tests.append(new_test)
    try:
        db.session.add_all(new_tests)
        db.session.commit()
    except DataError:
        raise

@API(version=3)
def report_test_start(
        session_id: int,
        name: str,
        file_name: (str, NoneType)=None,
        class_name: (str, NoneType)=None,
        test_logical_id: (str, NoneType)=None,
        scm: (str, NoneType)=None,
        file_hash: (str, NoneType)=None,
        scm_revision: (str, NoneType)=None,
        scm_dirty: bool=False,
        scm_local_branch: (str, NoneType)=None,
        scm_remote_branch: (str, NoneType)=None,
        is_interactive: bool=False,
        variation: (dict, NoneType)=None,
        metadata: (dict, NoneType)=None,
        test_index: (int, NoneType)=None,
        parameters: (dict, NoneType)=None,
):
    session = _validate_session(session_id)
    if test_index is None:
        test_index = Test.query.filter(Test.session_id == session_id).count() + 1
    returned = Test.query.filter(Test.logical_id == test_logical_id).first()
    if not returned or not test_logical_id:
        test_info_id = get_or_create_test_information_id(
            file_name=file_name, name=name, class_name=class_name)
        returned = Test(
            session_id=session.id,
            logical_id=test_logical_id,
            test_info_id=test_info_id,
        )
        if variation is not None:
            returned.test_variation = TestVariation(variation=sanitize_json(variation))
    returned.mark_started()
    returned.status = statuses.RUNNING
    returned.scm_dirty = scm_dirty
    returned.scm_revision = scm_revision
    returned.scm_local_branch = scm_local_branch
    returned.scm_remote_branch = scm_remote_branch
    returned.scm = scm
    returned.is_interactive = is_interactive
    returned.file_hash = file_hash
    returned.test_index = test_index
    returned.parameters = sanitize_json(parameters)
    if metadata is not None:
        for key, value in metadata.items():
            returned.metadatas.append(TestMetadata(key=key, metadata_item=value))

    try:
        db.session.add(returned)
        db.session.commit()
    except DataError:
        returned.test_variation.variation = sanitize_json(variation)
        db.session.add(returned)
        db.session.commit()
    metrics.num_new_tests.increment()
    return returned

@API
def report_test_distributed(
        session_id: int,
        test_logical_id: (str, NoneType)=None,
):
    session = _validate_session(session_id)
    test = Test.query.filter(Test.logical_id == test_logical_id).first()
    test.status = statuses.DISTRIBUTED

    try:
        db.session.add(test)
        db.session.commit()
    except DataError:
        pass
    return test


@API
def report_test_end(id: int, duration: (float, int)=None):
    test = Test.query.get(id)
    if test is None:
        abort(requests.codes.not_found)

    if test.end_time is not None:
        # we have a test, but it already ended
        error_abort('Test already ended', code=requests.codes.conflict)

    with updating_session_counters(test):
        if duration is None:
            test.mark_ended()
        else:
            test.mark_ended_at(test.start_time + duration)

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

        if test.interrupted and was_running:
            session_update['num_interrupted_tests'] = Session.num_interrupted_tests + 1

        if test.errored and (was_running or was_success):
            session_update['num_error_tests'] = Session.num_error_tests + 1

        if test.failed and (was_running or was_success):
            session_update['num_failed_tests'] = Session.num_failed_tests + 1

        if test.skipped and was_running:
            session_update['num_skipped_tests'] = Session.num_skipped_tests + 1

    if session_update:
        session = Session.query.filter(Session.id == test.session_id)
        session.update(session_update)
        parent_session = session.first().parent
        if parent_session:
            Session.query.filter(Session.id == parent_session.id).update(session_update)


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
def add_warning(message: str, filename: str=None, lineno: int=None, test_id: int=None, session_id: int=None, timestamp: (int, float)=None):
    # pylint: disable=superfluous-parens
    if not ((test_id is not None) ^ (session_id is not None)):
        error_abort('Either session_id or test_id required')
    if session_id is not None:
        obj = Session.query.get_or_404(session_id)
    else:
        obj = Test.query.get_or_404(test_id)
    if timestamp is None:
        timestamp = get_current_time()
    if obj.num_warnings < current_app.config['MAX_WARNINGS_PER_ENTITY']:
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
        obj = Session.query.get_or_404(session_id)
    else:
        obj = Test.query.get_or_404(test_id)

    returned = Comment(user_id=current_user.id, comment=comment)
    obj.comments.append(returned)

    obj.num_comments = type(obj).num_comments + 1
    db.session.add(obj)

    db.session.commit()
    return returned

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


################################################################################
## Search
