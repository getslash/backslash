from flask import Blueprint

from .models import Session, Test, TestError, SessionError
from weber_utils import paginated_view
from .filtering import filterable_view, Filter
from .rendering import auto_render, render_api_object
from .statuses import filter_query_by_session_status, filter_query_by_test_status
from .metadata import filter_test_metadata

import re
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')


def convert_typename(name):
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1).lower()

blueprint = Blueprint('rest', __name__)


def _register_rest_getters(objtype, filters=()):
    typename = convert_typename(objtype.__name__)
    @blueprint.route('/{0}s/<int:object_id>'.format(typename), endpoint='get_single_{0}'.format(typename))
    @auto_render
    def get_single_object(object_id):
        return objtype.query.get(object_id)

    @blueprint.route('/{0}s'.format(typename), endpoint='query_{0}s'.format(typename))
    @paginated_view(renderer=render_api_object)
    @filterable_view(filters, typename)
    def query_objects():
        return objtype.query


################################################################################

_register_rest_getters(Session, filters=[
    'product_name', 'product_version', 'user_name', 'logical_id',
    Filter('start_time', allowed_operators=('eq', 'ne', 'gt', 'lt', 'ge', 'le')),
    Filter('status', filter_func=filter_query_by_session_status)])

_register_rest_getters(Test, filters=[
    'name', 'logical_id', 'session_id',
    Filter('num_errors', allowed_operators=('eq', 'ne', 'gt', 'lt', 'ge', 'le')),
    Filter('num_failures', allowed_operators=('eq', 'ne', 'gt', 'lt', 'ge', 'le')),
    Filter('status', filter_func=filter_query_by_test_status),
    Filter('metadata', filter_func=filter_test_metadata, allowed_operators=('eq','exists'))])

_register_rest_getters(TestError, filters=[
    'test_id'])

_register_rest_getters(SessionError, filters=[
    'session_id'])

## more specific views

@blueprint.route('/sessions/<int:object_id>/tests', endpoint='get_tests_of_session')
@paginated_view(renderer=render_api_object)
def view_tests_of_session(object_id):
    return Test.query.filter(Test.session_id == object_id)
