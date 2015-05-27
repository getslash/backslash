from flask import Blueprint, request
from flask_restful import Api

from ..models import Session, Test, Error
from ..utils.rest import ModelResource


blueprint = Blueprint('rest', __name__, url_prefix='/rest')

rest = Api(blueprint)

def _resource(*args, **kwargs):
    def decorator(resource):
        rest.add_resource(resource, *args, **kwargs)
        return resource
    return decorator

################################################################################

@_resource('/sessions', '/sessions/<int:id>')
class SessionResource(ModelResource):

    MODEL = Session

