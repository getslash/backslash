import requests
from flask import abort
from models import Session, Test
from sqlalchemy import and_
from sqlalchemy import join

def filter_query_by_session_status(query, status):
    print 'status:',status
    if status not in ['RUNNING', 'FAILURE', 'SUCCESS']:
        abort(requests.codes.bad_request)
    if status == 'RUNNING':
        return query.filter_by(end_time=None)
    elif status == 'SUCCESS':
        from sqlalchemy.orm import aliased
        test = aliased(Test)
#        q = and_(Session.end_time != None, join(test, Session.tests).filter(and_(test.skipped == False,
#                                                                                 test.num_failures == 0,
#                                                                                 test.num_errors == 0)))
        q = and_(Session.end_time is not None, Session.logical_id == 'my_logical_id')
        print query.filter(q)
        return query.filter(q)
