from flask import request

from .models import Test

from .utils import statuses


def filter_by_statuses(cursor, model):
    if not _get_boolean_filter('show_unsuccessful', True):
        cursor = cursor.filter(model.status.in_((statuses.SUCCESS, statuses.SKIPPED, statuses.RUNNING)))
    if not _get_boolean_filter('show_successful', True):
        cursor = cursor.filter(model.status != statuses.SUCCESS)
    if not _get_boolean_filter('show_abandoned', True):
        if model is not Test:
            cursor = cursor.filter((model.end_time != None) & (model.num_finished_tests != 0))
    if not _get_boolean_filter('show_skipped', True):
        cursor = cursor.filter(model.status != statuses.SKIPPED)
    return cursor

def _get_boolean_filter(name, default):
    returned = request.args.get(name, None)
    if not returned:
        return default
    return returned.lower() in ('true', 'yes')
