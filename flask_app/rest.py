from flask import Blueprint

from .models import Session, Test
from weber_utils import paginated_view
from .rendering import auto_render, render_api_object

blueprint = Blueprint('rest', __name__)


def _register_rest_getters(objtype):
    typename = objtype.__name__.lower()
    @blueprint.route('/{0}s/<int:object_id>'.format(typename), endpoint='get_single_{0}'.format(typename))
    @auto_render
    def get_single_object(object_id):
        return objtype.query.get(object_id)

    @blueprint.route('/{0}s'.format(typename), endpoint='query_{0}s'.format(typename))
    @paginated_view(renderer=render_api_object)
    def query_objects():
        return objtype.query


def get_tests_of_session():
    @blueprint.route('/sessions/<int:object_id>/tests', endpoint='get_tests_of_session')
    @paginated_view(renderer=render_api_object)
    def get_tests_of_session(object_id):
        return Test.query.filter(Test.session_id == object_id)

################################################################################

_register_rest_getters(Session)
_register_rest_getters(Test)
get_tests_of_session()
