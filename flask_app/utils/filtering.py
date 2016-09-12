import json
import operator

from flask import request


def in_(field, value):
    return field.in_(value)

def notin_(field, value):
    return field.notin_(value)

class FilterConfig(object):

    def __init__(self, cfg):
        super(FilterConfig, self).__init__()
        self._cfg = cfg

    def filter(self, iterator, metadata):
        filter_json = self._get_filter_json()
        for filter_name, f in self._cfg.items():
            if f.default is not None and filter_name not in filter_json:
                filter_json[filter_name] = f.default

        for arg, value in filter_json.items():
            if arg not in self._cfg:
                continue
            f = self._cfg[arg]
            iterator = f.filter(iterator, value)
        return iterator

    def _get_filter_json(self):
        filter_json = request.args.get('filter', None)
        if filter_json is None:
            filter_json = {}
        else:
            try:
                filter_json = json.loads(filter_json)
            except ValueError:
                filter_json = {}
        return filter_json


class ConstFilter(object):

    def __init__(self, field, options, default=None):
        super(ConstFilter, self).__init__()
        self.field = field
        self.options = {
            opt_name: opt_val if isinstance(opt_val, tuple) else (operator.eq, opt_val)
            for opt_name, opt_val in options.items()
        }
        self.default = default

    def filter(self, iterator, value):
        operator, opt_val = self.options[value]
        iterator = iterator.filter(operator(self.field, opt_val))
        return iterator

class ToggleFilter(object):

    def __init__(self, field, default):
        super(ToggleFilter, self).__init__()
        self.field = field
        self.default = default

    def filter(self, iterator, value):
        iterator = iterator.filter(self.field == value)
        return iterator
