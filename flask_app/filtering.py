import functools
import operator

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
        filters[filter_obj.field_name] = filter_obj

    def decorator(func):

        @functools.wraps(func)
        def new_func(*args, **kwargs):
            returned = func(*args, **kwargs)
            # TODO: filters should be added to the query based on the filter order, not the request arg order
            for arg_name, filter_values in request.args.iterlists():
                if arg_name in _IGNORED_FIELD_NAMES:
                    continue
                for filter_value in filter_values:
                    filter_obj = filters.get(arg_name)
                    if filter_obj is None:
                        abort(requests.codes.bad_request)
                    returned = filter_obj.filter_query(returned, filter_value)
            return returned

        return new_func
    return decorator

class Filter(object):

    def __init__(self, field_name, filter_func=None, allowed_operators=('eq', 'ne')):
        super(Filter, self).__init__()
        self.field_name = field_name
        self.filter_func = filter_func
        self._allowed_operators = frozenset(allowed_operators)

    def filter_query(self, query, value):
        op, value = self._parse_op_and_value(value)
        if self.filter_func:
            if op is not operator.eq:
                abort(requests.codes.bad_request)
            return self.filter_func(query, value)
        field = self._deduce_queried_field(query)
        value = self._coerce_filter_value(field, value)
        return query.filter(op(field, value))

    def _coerce_filter_value(self, field, value):
        pythonic_type = field.property.columns[0].type.python_type
        if pythonic_type is bool:
            value = value.lower()
            if value not in ('true', 'false'):
                abort(requests.codes.bad_request)
            return value == 'true'
        return pythonic_type(value)

    def _parse_op_and_value(self, value):
        if ':' not in value:
            return operator.eq, value
        op_name, value = value.split(':', 1)
        if op_name not in self._allowed_operators:
            abort(requests.codes.bad_request)
        return getattr(operator, op_name), value

    def _deduce_queried_field(self, query):
        for d in query.column_descriptions:
            returned = getattr(d['type'], self.field_name, None)
            if returned is not None:
                return returned
        raise LookupError()
