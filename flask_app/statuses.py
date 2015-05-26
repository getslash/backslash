import requests
from flask import abort
from models import Session, Test
from sqlalchemy import or_, func


def filter_query_by_session_status(query, status):
    if status not in ['RUNNING', 'FAILURE', 'SUCCESS']:
        abort(requests.codes.bad_request)
    if status == 'RUNNING':
        regular_query = query.filter(Session.end_time == None).filter(Session.edited_status == None)
    elif status == 'SUCCESS':
        regular_query = query.filter(Test.session_id == Session.id).group_by(Session.id).\
            having(func.sum(Test.num_errors) == 0).having(func.sum(Test.num_failures) == 0).\
            filter(Session.end_time.isnot(None)).filter(Session.edited_status == None)
    elif status == 'FAILURE':
        regular_query = query.filter(Test.session_id == Session.id).group_by(Session.id).\
            having(or_(func.sum(Test.num_errors) > 0, func.sum(Test.num_failures) > 0)).\
            filter(Session.edited_status == None)

    edited_query = query.filter(Session.edited_status == status)
    return regular_query.union(edited_query)


def filter_query_by_test_status(query, status):
    if status not in ['RUNNING', 'SUCCESS', 'SKIPPED', 'FAILURE', 'ERROR', 'INTERRUPTED']:
        abort(requests.codes.bad_request)
    if status == 'RUNNING':
        regular_query = query.filter(Test.end_time == None).filter(Test.edited_status == None)
    elif status == 'SUCCESS':
        regular_query = query.filter(Test.end_time.isnot(None), Test.num_errors == 0, Test.num_failures == 0).\
            filter(Test.edited_status == None)
    elif status == 'FAILURE':
        regular_query = query.filter(Test.num_failures > 0).filter(Test.edited_status == None)
    elif status == 'ERROR':
        regular_query = query.filter(Test.num_errors > 0).filter(Test.edited_status == None)
    elif status == 'SKIPPED':
        regular_query = query.filter(Test.skipped).filter(Test.edited_status == None)
    elif status == 'INTERRUPTED':
        regular_query = query.filter(Test.interrupted).filter(Test.edited_status == None)

    edited_query = query.filter(Test.edited_status == status)
    return regular_query.union(edited_query)

