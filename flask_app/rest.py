from flask import Blueprint

from .models import Session, Test
from .api_utils import auto_render

blueprint = Blueprint('rest', __name__)


def _register_rest_getters(objtype):
    typename = objtype.__name__.lower()
    @blueprint.route('/{0}s/<int:object_id>'.format(typename), endpoint='get_single_{0}'.format(typename))
    @auto_render
    def get_single_object(object_id):
        return objtype.query.get(object_id)



################################################################################

_register_rest_getters(Session)
_register_rest_getters(Test)
