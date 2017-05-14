# pylint: disable=singleton-comparison
import flux
import sqlalchemy
from sqlalchemy import func

from flask import request

from .models import Test, Session

from .utils import statuses


class builders:

    @classmethod
    def build_successful_query(cls, model):
        return ~cls.build_unsuccessful_query(model)

    @classmethod
    def build_unsuccessful_query(cls, model):
        conds = [
            cls.build_status_query(model, statuses.INTERRUPTED),
            cls.build_abandoned_filter(model),
            model.num_errors != 0,
            model.num_failures != 0,
        ]
        if model is Session:
            conds.extend([
                model.num_error_tests != 0,
                model.num_failed_tests != 0,
                sqlalchemy.and_(model.end_time != None, model.num_finished_tests == 0),
                sqlalchemy.and_(model.total_num_tests != 0, model.total_num_tests != model.num_finished_tests)
            ])
        return sqlalchemy.or_(*conds)

    @classmethod
    def build_abandoned_filter(cls, model):
        return sqlalchemy.and_(
            model.end_time == None,
            model.next_keepalive != None,
            model.next_keepalive < flux.current_timeline.time())

    @classmethod
    def build_status_query(cls, model, status):
        return func.lower(model.status) == status.lower()


def filter_by_statuses(cursor, model):

    if not _get_boolean_filter('show_unsuccessful', True):
        cursor = cursor.filter(~builders.build_unsuccessful_query(model))
    if not _get_boolean_filter('show_successful', True):
        cursor = cursor.filter(~builders.build_successful_query(model))
    if not _get_boolean_filter('show_planned', False):
        cursor = cursor.filter(~builders.build_status_query(model, statuses.PLANNED))
    if not _get_boolean_filter('show_abandoned', True):
        cursor = cursor.filter(~builders.build_abandoned_filter(model))
    if not _get_boolean_filter('show_skipped', True):
        if model is Session:
            cursor = cursor.filter(model.num_skipped_tests == 0)
        elif model is Test:
            cursor = cursor.filter(~builders.build_status_query(model, statuses.SKIPPED))
    return cursor

def _get_boolean_filter(name, default):
    returned = request.args.get(name, None)
    if not returned:
        return default
    return returned.lower() in ('true', 'yes')
