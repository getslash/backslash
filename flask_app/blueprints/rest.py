import requests
from flask import abort, Blueprint, request, session

from flask_restful import Api, reqparse

from ..models import Error, Session, Test, User
from ..utils.rest import ModelResource

blueprint = Blueprint('rest', __name__, url_prefix='/rest')

rest = Api(blueprint)


def _resource(*args, **kwargs):
    def decorator(resource):
        rest.add_resource(resource, *args, **kwargs)
        return resource
    return decorator

##########################################################################


@_resource('/sessions', '/sessions/<int:object_id>')
class SessionResource(ModelResource):

    MODEL = Session


@_resource('/tests', '/tests/<int:object_id>', '/sessions/<int:session_id>/tests')
class TestResource(ModelResource):

    MODEL = Test

    def _get_iterator(self):
        session_id = request.view_args.get('session_id')
        if session_id is not None:
            return Test.query.filter(Test.session_id == session_id)
        return super(TestResource, self)._get_iterator()


@_resource('/errors')
class ErrorResource(ModelResource):

    MODEL = Error

    def _get_iterator(self):
        args = error_query_parser.parse_args()
        if args.session_id is not None:
            return Error.query.join((Session, Error.session)).filter(Session.id == args.session_id)
        elif args.test_id is not None:
            return Error.query.join((Test, Error.test)).filter(Test.id == args.test_id)
        abort(requests.codes.bad_request)


@_resource('/users', '/users/<int:object_id>')
class UserResource(ModelResource):

    ONLY_FIELDS = ['id', 'email']
    MODEL = User

    def _get_iterator(self):
        abort(requests.codes.unauthorized)

    def _get_object_by_id(self, object_id):
        if object_id != session.get('user_id'):
            abort(requests.codes.unauthorized)
        return User.query.get_or_404(int(object_id))


error_query_parser = reqparse.RequestParser()
error_query_parser.add_argument('session_id', type=int, default=None)
error_query_parser.add_argument('test_id', type=int, default=None)
