from flask import Blueprint

from .models import Session
from .api_utils import auto_render

blueprint = Blueprint('rest', __name__)


def _register_rest_getters(objtype):
    @blueprint.route('/{0}s/<int:object_id>'.format(objtype.__name__.lower()))
    @auto_render
    def get_single_object(object_id):
        return objtype.query.get(object_id)



################################################################################

_register_rest_getters(Session)
