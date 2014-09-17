import functools

from flask import Response

from .models import db
from .rendering import render_api_object
from .responses import API_SUCCESS, API_RESPONSE



def get_api_decorator(blueprint):
    """Creates a utility decorator for adding routes to an API blueprint
    """

    def decorator(func, name=None):
        if isinstance(func, str):
            return functools.partial(decorator, name=func)
        if name is None:
            name = func.__name__

        @functools.wraps(func)
        def new_func(*args, **kwargs):
            returned = func(*args, **kwargs)
            if returned is None:
                returned = API_SUCCESS()
            elif not isinstance(returned, Response):
                returned = API_RESPONSE(render_api_object(returned))
            return returned

        return blueprint.route('/{0}'.format(name), methods=['post'])(new_func)

    return decorator


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
