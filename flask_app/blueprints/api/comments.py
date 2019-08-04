from .blueprint import API
from flask_security import current_user
from flask import g
from ...models import Session, Test, db, Comment


@API
def post_comment(comment: str, session_id: int=None, test_id: int=None):
    if not (session_id is not None) ^ (test_id is not None):
        error_abort('Either session_id or test_id required')

    if session_id is not None:
        obj = Session.query.get_or_404(session_id)
    else:
        obj = Test.query.get_or_404(test_id)
    user_id = current_user.get_id() or g.token_user.get_id()
    returned = Comment(user_id=user_id, comment=comment)
    obj.comments.append(returned)

    obj.num_comments = type(obj).num_comments + 1
    db.session.add(obj)

    db.session.commit()
    return returned
