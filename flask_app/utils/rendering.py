import datetime
import functools

import inflect

from .responses import API_SUCCESS
from .english import plural_noun


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

    for method_name in dir(obj):
        method = getattr(obj, method_name)
        if is_computed_field(method):
            returned[method_name] = method()

    returned['type'] = typename = obj.get_typename()
    returned['api_path'] = '/rest/{}/{}'.format(plural_noun(typename), obj.id)
    return returned


def computed_field(func):
    func.__computed__ = True
    return func

def is_computed_field(method):
    return hasattr(method, '__computed__')


def render_api_value(value):
    if isinstance(value, datetime.datetime):
        value = (value - datetime.datetime.utcfromtimestamp(0)).total_seconds()
    return value
