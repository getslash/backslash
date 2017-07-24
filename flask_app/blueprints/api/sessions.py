import requests

from flask import g, request
from flask_simple_api import error_abort

from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from ...auth import get_or_create_user

from ...models import Session, db, SessionMetadata
from ...utils import get_current_time, statuses
from ...utils.subjects import get_or_create_subject_instance
from ...utils.users import has_role
from ... import metrics
from .blueprint import API

NoneType = type(None)


@API(version=2)
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
                         ):
    if hostname is None:
        hostname = request.remote_addr

    # fix user identification
    if user_email is not None and user_email != g.token_user.email:
        if not has_role(g.token_user.id, 'proxy'):
            error_abort('User {} is not authorized to run tests on others behalf. Tried running as {}'.format(g.token_user.email, user_email),
                        code=requests.codes.forbidden)
        real_user_id = g.token_user.id
        user_id = get_or_create_user({'email': user_email}).id
    else:
        user_id = g.token_user.id
        real_user_id = None

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
        next_keepalive=None if keepalive_interval is None else get_current_time() +
        keepalive_interval,
    )

    returned.mark_started()

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
            subject.subject.last_activity = get_current_time()
            db.session.add(subject)

    if metadata is not None:
        for key, value in metadata.items():
            returned.metadata_items.append(SessionMetadata(
                session=returned, key=key, metadata_item=value))

    db.session.add(returned)
    metrics.num_new_sessions.increment()
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        if parent_logical_id:
            Session.query.filter_by(logical_id=parent_logical_id).first_or_404()
        error_abort('Tried to report a session which conflicts with an existing session', code=requests.codes.conflict)
    return returned


@API(version=2)
def report_session_end(id: int, duration: (int, NoneType)=None, has_fatal_errors: bool=False):
    try:
        session = Session.query.filter(Session.id == id).one()
    except NoResultFound:
        error_abort('Session not found', code=requests.codes.not_found)

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
    timestamp = get_current_time() + s.keepalive_interval
    s.next_keepalive = timestamp
    s.extend_timespan_to(timestamp)
    for test in Test.query.filter(session_id=session_id, end_time=None):
        test.extend_timespan_to(timestamp)
    db.session.add(s)
    db.session.commit()


@API
def report_session_interrupted(id: int):
    s = Session.query.get_or_404(id)
    if s.end_time is not None:
        error_abort('Ended session cannot be marked as interrupted',
                    code=requests.codes.conflict)
    s.status = statuses.INTERRUPTED
    if s.parent:
        s.parent.status = statuses.INTERRUPTED
    db.session.add(s)
    db.session.commit()
