from .caching import cache
from .. import models

from flask import abort

from sqlalchemy.orm.exc import NoResultFound

@cache.cache_on_arguments()
def get_user_id_by_email(email):
    try:
        return models.User.query.filter_by(email=email).one().id
    except NoResultFound:
        abort(404)

def has_role(user, role):
    if isinstance(user, int):
        user = models.User.query.get(user)
        if user is None:
            return False
    user_roles = {r.name for r in user.roles}
    if 'admin' in user_roles:
        return True
    return role in user_roles
