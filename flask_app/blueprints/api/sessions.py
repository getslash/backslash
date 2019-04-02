from flask import g, request
from flask_simple_api import error_abort
import flux
import requests

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from ...auth import get_or_create_user

from ...search import get_orm_query_from_search_string
from ...models import Session, Test, db, SessionMetadata, User
from ...utils import get_current_time, statuses
from ...utils.api_utils import requires_role
from ...utils.subjects import get_or_create_subject_instance
from ...utils.users import has_role
from ...utils import profiling
from .blueprint import API

NoneType = type(None)

_DEFAULT_DELETE_GRACE_PERIOD_SECONDS = 60 * 60 * 24 * 30


@API(version=3)
def report_session_start(logical_id: str=None,
                         parent_logical_id: (NoneType, str)=None,
                         is_parent_session: bool=False,
                         child_id: (NoneType, str)=None,
                         hostname: str=None,
                         total_num_tests: int=None,
                         metadata: dict=None,
                         user_email: str=None,
                         keepalive_interval: (NoneType, int)=None,
                         subjects: (list, NoneType)=None,
                         infrastructure: (str, NoneType)=None,
                         ttl_seconds: (int, NoneType)=None,
                         ):
    if hostname is None:
        hostname = request.remote_addr

    # fix user identification
    if user_email is not None and user_email != g.token_user.email:
        if not has_role(g.token_user.id, 'proxy'):
            error_abort('User {} is not authorized to run tests on others behalf. Tried running as {}'.format(g.token_user.email, user_email),
                        code=requests.codes.forbidden)
        real_user_id = g.token_user.id
        real_user = get_or_create_user({'email': user_email})
        user_id = real_user.id
    else:
        user_id = g.token_user.id
        real_user = None
        real_user_id = None

    if keepalive_interval is None and ttl_seconds is not None:
        error_abort("Cannot specify session TTL when keepalive isn't used")

    returned = Session(
        hostname=hostname,
        parent_logical_id=parent_logical_id,
        is_parent_session=is_parent_session,
        child_id=child_id,
        total_num_tests=total_num_tests,
        infrastructure=infrastructure,
        user_id=user_id,
        real_user_id=real_user_id,
        status=statuses.RUNNING,
        logical_id=logical_id,
        keepalive_interval=keepalive_interval,
        ttl_seconds=ttl_seconds,
    )

    if real_user is not None:
        real_user.last_activity = flux.current_timeline.time()

    returned.mark_started()

    returned.update_keepalive()

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
            db.session.add(subject)

        assert list(returned.subject_instances)
        returned.notify_subject_activity()

    if metadata is not None:
        for key, value in metadata.items():
            returned.metadata_items.append(SessionMetadata(
                session=returned, key=key, metadata_item=value))

    db.session.add(returned)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        if parent_logical_id:
            Session.query.filter_by(logical_id=parent_logical_id).first_or_404()
        error_abort('Tried to report a session which conflicts with an existing session', code=requests.codes.conflict)
    profiling.notify_session_start()
    return returned


@API(version=2)
def report_session_end(id: int, duration: (int, NoneType)=None, has_fatal_errors: bool=False):
    try:
        session = Session.query.filter(Session.id == id).one()
    except NoResultFound:
        error_abort('Session not found', code=requests.codes.not_found)
    session.notify_subject_activity()

    if session.status not in (statuses.RUNNING, statuses.INTERRUPTED):
        error_abort('Session is not running', code=requests.codes.conflict)

    if duration is None:
        session.mark_ended()
    else:
        session.mark_ended_at(session.start_time + duration)

    # TODO: handle interrupted sessions
    if session.num_error_tests or session.num_errors:
        session.status = statuses.ERROR
    elif session.num_failed_tests or session.num_failures:
        session.status = statuses.FAILURE
    elif session.status != statuses.INTERRUPTED:
        session.status = statuses.SUCCESS
    session.has_fatal_errors = has_fatal_errors
    session.in_pdb = False
    if session.ttl_seconds is not None:
        session.delete_at = flux.current_timeline.time() + session.ttl_seconds
    db.session.add(session)
    db.session.commit()


@API
def report_in_pdb(session_id: int):
    s = Session.query.get_or_404(session_id)
    s.in_pdb = True
    db.session.add(s)
    db.session.commit()


@API
def report_not_in_pdb(session_id: int):
    s = Session.query.get_or_404(session_id)
    s.in_pdb = False
    db.session.add(s)
    db.session.commit()


@API
def send_keepalive(session_id: int):
    s = Session.query.get_or_404(session_id)
    if s.end_time is not None:
        return

    if s.keepalive_interval is not None:
        timestamp = get_current_time() + s.keepalive_interval
        s.update_keepalive()
        for test in Test.query.filter(Test.session_id==session_id,
                                      Test.end_time == None,
                                      Test.start_time != None):
            test.extend_timespan_to(timestamp)
    s.notify_subject_activity()
    db.session.commit()


@API
def report_session_interrupted(id: int):
    s = Session.query.get_or_404(id)
    s.status = statuses.INTERRUPTED
    if s.parent:
        s.parent.status = statuses.INTERRUPTED
    db.session.commit()


@API(require_real_login=True)
@requires_role("admin")
def discard_session(
    session_id: int, grace_period_seconds: int = _DEFAULT_DELETE_GRACE_PERIOD_SECONDS
):
    session = Session.query.get_or_404(session_id)

    delete_at = flux.current_timeline.time() + grace_period_seconds  # pylint: disable=undefined-variable
    Session.query.filter(
        (Session.parent_logical_id == session.logical_id) | (Session.id == session.id)
    ).update({Session.delete_at: delete_at}, synchronize_session=False)
    db.session.commit()


@API(require_real_login=True)
@requires_role('admin')
def discard_sessions_search(search_string: str, grace_period_seconds: int=_DEFAULT_DELETE_GRACE_PERIOD_SECONDS):
    if not search_string:
        error_abort('Invadlid search string')
    delete_at = flux.current_timeline.time() + grace_period_seconds
    search_query = get_orm_query_from_search_string('session', search_string).filter(Session.delete_at == None)
    Session.query.filter(Session.id.in_(db.session.query(search_query.subquery().c.id))).update({
        'delete_at': delete_at
    }, synchronize_session=False)
    db.session.commit()


@API(require_real_login=True)
@requires_role("admin")
def preserve_session(session_id: int):
    session = Session.query.get_or_404(session_id)
    Session.query.filter(
        (Session.parent_logical_id == session.logical_id) | (Session.id == session.id)
    ).update({Session.delete_at: None}, synchronize_session=False)
    db.session.commit()


@API
def report_reporting_stopped(session_id: int):
    session = Session.query.get_or_404(session_id)
    session.reporting_stopped = True
    db.session.commit()
