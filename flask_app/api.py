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
@takes_schema_args(logical_id=int,
                   name=str,
                   version=Optional(str),
                   revision=Optional(str))
def set_product(logical_id, name, version=None, revision=None):
    update = {'product_name': name, 'product_version': version, 'product_revision': revision}
    try:
        Session.query.filter(Session.logical_id == logical_id).update(update)
    except NoResultFound:
        abort(requests.codes.not_found)

@api_func
@auto_commit
@takes_schema_args(logical_id=int,
                   hostname=Optional(str),
                   product_name=Optional(str),
                   product_version=Optional(str),
                   product_revision=Optional(str))
def report_session_start(logical_id, hostname=None,
                         product_name=None,
                         product_version=None,
                         product_revision=None):
    if hostname is None:
        hostname = request.remote_addr
    return Session(logical_id=logical_id, hostname=hostname,
                   product_name=product_name, product_version=product_version, product_revision=product_revision)


@api_func
@auto_commit
@takes_schema_args(logical_id=int, duration=Optional((float, int)))
def report_session_end(logical_id, duration=None):
    update = {'end_time': get_current_time() if duration is None else Session.start_time + duration}
    if not Session.query.filter(Session.logical_id == logical_id, Session.end_time == None).update(update):
        if Session.query.filter(Session.logical_id == logical_id).count():
            # we have a session, but it already ended
            abort(requests.codes.conflict)
        else:
            abort(requests.codes.not_found)


@api_func
@auto_commit
@takes_schema_args(session_logical_id=int, test_logical_id=int, name=str)
def report_test_start(session_logical_id, test_logical_id, name):
    try:
        session = Session.query.filter(Session.logical_id == session_logical_id).one()
    except NoResultFound:
        abort(requests.codes.not_found)
    if session.end_time is not None:
        abort(requests.codes.conflict)
    return Test(session_id=session.id, logical_id=test_logical_id, name=name)


@api_func
@auto_commit
@takes_schema_args(logical_id=int, duration=Optional((float, int)))
def report_test_end(logical_id, duration=None):
    update = {'end_time': get_current_time() if duration is None else Test.start_time + duration}
    if not Test.query.filter(Test.logical_id == logical_id, Test.end_time == None).update(update):
        if Test.query.filter(Test.logical_id == logical_id).count():
            # we have a test, but it already ended
            abort(requests.codes.conflict)
        else:
            abort(requests.codes.not_found)
