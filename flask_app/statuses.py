import requests
from flask import abort
from models import Session, Test
from sqlalchemy import or_, func


def filter_query_by_session_status(query, status):
    if status not in ['RUNNING', 'FAILURE', 'SUCCESS']:
        abort(requests.codes.bad_request)
    if status == 'RUNNING':
        return query.filter_by(end_time=None)
    elif status == 'SUCCESS':
        return query.filter(Test.session_id == Session.id).group_by(Session.id).\
            having(func.sum(Test.num_errors) == 0).having(func.sum(Test.num_failures) == 0).\
            filter(Session.end_time.isnot(None))
    elif status == 'FAILURE':
        return query.filter(Test.session_id == Session.id).group_by(Session.id).\
            having(or_(func.sum(Test.num_errors) > 0, func.sum(Test.num_failures) > 0))


def filter_query_by_test_status(query, status):
    if status not in ['RUNNING', 'SUCCESS', 'SKIPPED', 'FAILURE', 'ERROR']:
        abort(requests.codes.bad_request)
    if status == 'RUNNING':
        return query.filter_by(end_time=None)
    elif status == 'SUCCESS':
        return query.filter(Test.end_time.isnot(None), Test.num_errors == 0, Test.num_failures == 0)
    elif status == 'FAILURE':
        return query.filter(Test.num_failures > 0)
    elif status == 'ERROR':
        return query.filter(Test.num_errors > 0)
    elif status == 'SKIPPED':
        return query.filter(Test.skipped)



def get_session_status(session):
    if session.end_time is None:
        return 'RUNNING'
    else:
        for test in session.tests:
            if test.status() == 'FAILURE' or test.status() == 'ERROR':
                return 'FAILURE'
        return 'SUCCESS'
