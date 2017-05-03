# pylint: disable=singleton-comparison
import flux
import sqlalchemy

from flask import request

from .models import Test, Session

from .utils import statuses


def filter_by_statuses(cursor, model):
    if not _get_boolean_filter('show_unsuccessful', True):
        cursor = cursor.filter(model.status.in_((statuses.SUCCESS, statuses.SKIPPED, statuses.RUNNING)))
    if not _get_boolean_filter('show_successful', True):
        cursor = cursor.filter(model.status != statuses.SUCCESS)
    if not _get_boolean_filter('show_planned', False):
        cursor = cursor.filter(model.status != statuses.PLANNED)
    if not _get_boolean_filter('show_abandoned', True):
        if model is not Test:
            cursor = cursor.filter(
                sqlalchemy.not_(
                    sqlalchemy.and_(
                        model.end_time == None,
                        model.next_keepalive != None,
                        model.next_keepalive < flux.current_timeline.time())))
    if not _get_boolean_filter('show_skipped', True):
        if model is Session:
            cursor = cursor.filter(model.num_skipped_tests == 0)
        elif model is Test:
            cursor = cursor.filter(model.status != statuses.SKIPPED)
    return cursor

def _get_boolean_filter(name, default):
    returned = request.args.get(name, None)
    if not returned:
        return default
    return returned.lower() in ('true', 'yes')
