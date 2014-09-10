import datetime
import functools

from flask import jsonify, Response

from .models import db


def API_RESPONSE(rv=None, metadata=None, error=None):
    return jsonify({
        'error': error,
        'result': rv,
        'metadata': metadata,
    })

API_SUCCESS = API_RESPONSE


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


def auto_render(func):
    """Automatically renders returned objects using render_api_object
    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        return API_SUCCESS(render_api_object(func(*args, **kwargs)))

    return new_func


def render_api_object(obj):
    returned = {c.name: render_api_value(obj.__getattribute__(c.name))
                for c in obj.__table__.columns}
    returned['type'] = typename = type(obj).__name__.lower()
    returned['api_path'] = '/rest/{0}s/{1}'.format(typename, obj.id)
    return returned

def render_api_value(value):
    if isinstance(value, datetime.datetime):
        value = (value - datetime.datetime.utcfromtimestamp(0)).total_seconds()
    return value
