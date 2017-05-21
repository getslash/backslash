from ..models import Test, Session, db

def parse_session_id(session_id):
    return _parse_id(Session, session_id)

def parse_test_id(test_id):
    return _parse_id(Test, test_id)

def _parse_id(objtype, obj_id):
    try:
        numeric_id = int(obj_id)
    except ValueError:
        numeric_id = None

    q = objtype.logical_id == str(obj_id)
    if numeric_id is not None:
        q = (objtype.id == numeric_id) | q
    return db.session.query(objtype.id).filter(q).first_or_404()[0]
