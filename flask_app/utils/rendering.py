import functools
import datetime

from .english import plural_noun



def render_api_object(obj, only_fields=None, extra_fields=None, is_single=False):
    if only_fields is None:
        only_fields = [c.name for c in obj.__table__.columns]
    returned = {}
    for field_name in only_fields:
        column = obj.__table__.columns[field_name]
        value = render_api_value(obj.__getattribute__(field_name))

        try:
            python_type = column.type.python_type
        except NotImplementedError:
            continue

        if value is None and python_type is bool and column.default is not None:
            value = column.default.arg
        returned[field_name] = value

    if extra_fields is not None:
        for field_name, attr in extra_fields.items():
            value = obj
            for p in attr.split('.'):
                value = getattr(value, p)
            returned[field_name] = value

    objtype = type(obj)
    for method_name in dir(objtype):
        method = getattr(objtype, method_name)
        if is_single:
            should_include = is_rendered_on_single(method)
        else:
            should_include = is_rendered_on_all(method)

        if should_include:
            rendered_name = method.__rendered__.get('name', method_name)
            returned[rendered_name] = getattr(obj, method_name)()

    returned['type'] = typename = obj.get_typename()
    returned['api_path'] = '/rest/{}/{}'.format(plural_noun(typename), obj.id)
    return returned


def rendered_field(func=None, name=None):
    if func is None:
        return functools.partial(rendered_field, name=name)
    if name is None:
        name = func.__name__
    func.__rendered__ = {'on': 'all', 'name': name}
    return func


def rendered_only_on_single(func):
    func.__rendered__ = {'on': 'single'}
    return func


def is_rendered_on_all(method):
    return getattr(method, '__rendered__', {}).get('on') == 'all'


def is_rendered_on_single(method):
    return getattr(method, '__rendered__', {}).get('on') in ('single', 'all')


def render_api_value(value):
    if isinstance(value, datetime.datetime):
        value = (value - datetime.datetime.utcfromtimestamp(0)).total_seconds()
    return value
