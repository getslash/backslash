import functools

from flask import Response

from ..models import db
from .responses import API_SUCCESS, API_RESPONSE
from .rendering import render_api_object


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
        if returned is not None:
            db.session.add(returned)
        db.session.commit()
        return returned

    return new_func
