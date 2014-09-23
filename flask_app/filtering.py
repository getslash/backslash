import functools

import requests
from flask import abort, request

_IGNORED_FIELD_NAMES = frozenset(['page', 'page_size'])

def filterable_view(filterable_fields):
    """Makes a view returning an SQLAlchemy query filterable

    :param filterable_fields: A list of either field names to enable filtering by, or :class:`Filter` objects
    controlling how the filtering is done
    """

    filters = {}
    for filter_obj in filterable_fields:
        if not isinstance(filter_obj, Filter):
            filter_obj = Filter(filter_obj)
        filters[filter_obj.name] = filter_obj

    def decorator(func):

        @functools.wraps(func)
        def new_func(*args, **kwargs):
            returned = func(*args, **kwargs)
            for arg_name, filter_value in request.args.items():
                if arg_name in _IGNORED_FIELD_NAMES:
                    continue
                filter_obj = filters.get(arg_name)
                if filter_obj is None:
                    abort(requests.codes.bad_request)
                returned = filter_obj.filter_query(returned, filter_value)
            return returned

        return new_func
    return decorator

class Filter(object):

    def __init__(self, name):
        super(Filter, self).__init__()
        self.name = name

    def filter_query(self, query, value):
        return query.filter_by(**{self.name: value})
