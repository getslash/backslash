import functools

import requests
from flask import request, abort
from flask.ext.security import login_user

from sqlalchemy.orm.exc import NoResultFound

from ..models import db, User, RunToken
from .rendering import render_api_object
from .responses import API_RESPONSE, API_SUCCESS


def auto_render(func):
    """Automatically renders returned object"""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        returned = func(*args, **kwargs)
        if isinstance(returned, db.Model):
            returned = render_api_object(returned)
        return returned
    return new_func


def auto_commit(func):
    """Automatically commits to the database on success, possibly adding the returned object beforehand
    """
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        returned = func(*args, **kwargs)
        if isinstance(returned, db.Model):
            db.session.add(returned)
        db.session.commit()
        return returned

    return new_func


def requires_runtoken(func):
    """Logs a user in based on his/her run token
    Fails the request if a run token wasn't specified or is invalid
    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        user = _get_user_from_run_token()
        login_user(user)
        return func(*args, **kwargs)
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
