import functools

import requests
from flask import request, abort, g
from flask_simple_api import error_abort
from flask_login import login_user, logout_user, current_user

from sqlalchemy.orm.exc import NoResultFound

from .users import has_role
from ..models import db, User, RunToken
from .rendering import render_api_object
from .responses import API_RESPONSE, API_SUCCESS


def auto_render(func):
    """Automatically renders returned object"""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        returned = func(*args, **kwargs)
        if isinstance(returned, db.Model):
            returned = render_api_object(returned, is_single=True)
        return returned
    return new_func


def requires_login(func):
    return requires_login_or_runtoken(func, allow_runtoken=False)


def requires_role(role):
    needed = {role}
    def decorator(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            if not has_role(current_user, role):
                abort(requests.codes.forbidden)
            return func(*args, **kwargs)
        return new_func
    return decorator



def requires_login_or_runtoken(func, allow_runtoken=True):
    """Logs a user in based on his/her run token, assuming the user isn't already logged in.
    Fails the request if a run token wasn't specified or is invalid
    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        if not current_user.is_authenticated:
            if not allow_runtoken:
                error_abort('Run token not alowed for API', code=requests.codes.unauthorized)
            g.token_user = _get_user_from_run_token()
        try:
            return func(*args, **kwargs)
        finally:
            if hasattr(g, 'token_user'):
                del g.token_user
    return new_func

def _get_user_from_run_token():
    token = request.headers.get('X-Backslash-run-token', None)
    if token is None:
        abort(requests.codes.unauthorized)
    try:
        user = User.query.join(RunToken).filter(RunToken.token==token).one()
    except NoResultFound:
        abort(requests.codes.unauthorized)
    return user
