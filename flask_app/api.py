import datetime

import requests
from flask import abort, Blueprint, request

from weber_utils import Optional, takes_schema_args

from .api_utils import auto_commit, get_api_decorator
from .utils import get_current_time
from .models import Session, Test
from sqlalchemy.orm.exc import NoResultFound

blueprint = Blueprint('api', __name__)

api_func = get_api_decorator(blueprint)

##########################################################################


@api_func
@auto_commit
@takes_schema_args(hostname=Optional(str))
def report_session_start(hostname=None):
    if hostname is None:
        hostname = request.remote_addr
    return Session(hostname=hostname)


@api_func
@auto_commit
@takes_schema_args(id=int, duration=Optional((float, int)))
def report_session_end(id, duration=None):
    update = {'end_time': get_current_time(
    ) if duration is None else Session.start_time + datetime.timedelta(seconds=duration)}
    if not Session.query.filter(Session.id == id, Session.end_time == None).update(update):
        if Session.query.filter(Session.id == id).count():
            # we have a session, but it already ended
            abort(requests.codes.conflict)
        else:
            abort(requests.codes.not_found)


@api_func
@auto_commit
@takes_schema_args(session_id=int, name=str)
def report_test_start(session_id, name):
    try:
        session = Session.query.filter(Session.id == session_id).one()
    except NoResultFound:
        abort(requests.codes.not_found)
    if session.end_time is not None:
        abort(requests.codes.conflict)
    return Test(session_id=session_id, name=name)


@api_func
@auto_commit
@takes_schema_args(id=int, duration=Optional((float, int)))
def report_test_end(id, duration=None):
    update = {'end_time': get_current_time(
    ) if duration is None else Test.start_time + datetime.timedelta(seconds=duration)}
    if not Test.query.filter(Test.id == id, Test.end_time == None).update(update):
        if Test.query.filter(Test.id == id).count():
            # we have a test, but it already ended
            abort(requests.codes.conflict)
        else:
            abort(requests.codes.not_found)
