# pylint: disable=bad-whitespace
from flask import current_app
from flask_simple_api import error_abort
from .blueprint import API
from ...models import Session, Warning, Test, db
from ...utils import get_current_time
from sqlalchemy import func, distinct

@API
def add_warning(message:str, filename:str=None, lineno:int=None, test_id:int=None, session_id:int=None, timestamp:(int,float)=None):
    # pylint: disable=superfluous-parens
    if not ((test_id is not None) ^ (session_id is not None)):
        error_abort('Either session_id or test_id required')

    if session_id is not None:
        obj = Session.query.get_or_404(session_id)
    else:
        obj = Test.query.get_or_404(test_id)

    if timestamp is None:
        timestamp = get_current_time()

    warning = Warning.query.filter_by(session_id=session_id, test_id=test_id, lineno=lineno, filename=filename, message=message).first()
    if warning is None:
        num_distinct_warnings = db.session.query(Warning.lineno, Warning.filename, Warning.message).filter_by(session_id=session_id, test_id=test_id).distinct().count()
        if num_distinct_warnings < current_app.config['MAX_WARNINGS_PER_ENTITY']:
            warning = Warning(message=message, timestamp=timestamp, filename=filename, lineno=lineno, test_id=test_id, session_id=session_id)
            db.session.add(warning)

    else:
        warning.num_warnings = Warning.num_warnings + 1
        warning.timestamp = timestamp

    obj.num_warnings = type(obj).num_warnings + 1
    if session_id is None:
        obj.session.num_test_warnings = Session.num_test_warnings + 1
        db.session.add(obj.session)

    db.session.commit()
