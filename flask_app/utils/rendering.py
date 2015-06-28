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


def render_api_object(obj, only_fields=None, extra_fields=None):
    if only_fields is None:
        only_fields = [c.name for c in obj.__table__.columns]
    returned = {field_name: render_api_value(obj.__getattribute__(field_name))
                for field_name in only_fields}

    if extra_fields is not None:
        for field_name, attr in extra_fields.items():
            value = obj
            for p in attr.split('.'):
                value = getattr(value, p)
            returned[field_name] = value

    for method_name in dir(obj):
        method = getattr(obj, method_name)
        if is_rendered_field(method):
            returned[method_name] = method()

    returned['type'] = typename = obj.get_typename()
    returned['api_path'] = '/rest/{}/{}'.format(plural_noun(typename), obj.id)
    return returned


def rendered_field(func):
    func.__rendered__ = True
    return func

def is_rendered_field(method):
    return hasattr(method, '__rendered__')


def render_api_value(value):
    if isinstance(value, datetime.datetime):
        value = (value - datetime.datetime.utcfromtimestamp(0)).total_seconds()
    return value
