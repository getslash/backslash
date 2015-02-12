from flask import Blueprint

from .models import Session, Test
from weber_utils import paginated_view
from .filtering import filterable_view, Filter
from .rendering import auto_render, render_api_object
from .statuses import filter_query_by_session_status, filter_query_by_test_status
from .metadata import filter_test_metadata

blueprint = Blueprint('rest', __name__)


def _register_rest_getters(objtype, filters=()):
    typename = objtype.__name__.lower()
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

## more specific views

@blueprint.route('/sessions/<int:object_id>/tests', endpoint='get_tests_of_session')
@paginated_view(renderer=render_api_object)
def view_tests_of_session(object_id):
    return Test.query.filter(Test.session_id == object_id)
