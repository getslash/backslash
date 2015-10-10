import operator

import requests

from flask import Blueprint, abort, request, session
from flask.ext.security.core import current_user
from flask_restful import Api, reqparse
from sqlalchemy import text
from sqlalchemy.orm.exc import NoResultFound

from .. import models
from ..models import Comment, Error, Session, Test, User, Activity
from ..utils.rest import ModelResource
from ..utils import statuses

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
    DEFAULT_SORT = (Session.start_time.desc(),)
    from .filter_configs import SESSION_FILTERS as FILTER_CONFIG

    def _get_iterator(self):
        returned = super(SessionResource, self)._get_iterator()
        if request.args.get('show_archived') != 'true':
            returned = returned.filter(Session.archived == False)
        return returned

@_resource('/tests', '/tests/<int:object_id>', '/sessions/<int:session_id>/tests')
class TestResource(ModelResource):

    MODEL = Test
    DEFAULT_SORT = (Test.start_time.desc(),)
    from .filter_configs import TEST_FILTERS as FILTER_CONFIG

    def _get_iterator(self):
        session_id = request.args.get('session_id')
        if session_id is None:
            session_id = request.view_args.get('session_id')
        if session_id is not None:
            return Test.query.filter(Test.session_id == session_id).order_by(*self.DEFAULT_SORT)
        return super(TestResource, self)._get_iterator()

warnings_parser = reqparse.RequestParser()
warnings_parser.add_argument('session_id', type=int, default=None)
warnings_parser.add_argument('test_id', type=int, default=None)


@_resource('/warnings', '/warnings/<int:object_id>')
class WarningsResource(ModelResource):

    MODEL = models.Warning
    DEFAULT_SORT = (models.Warning.timestamp.desc(),)

    def _get_iterator(self):
        args = warnings_parser.parse_args()
        returned = self.MODEL.query.filter_by(test_id=args.test_id, session_id=args.session_id)
        return returned


session_test_user_query_parser = reqparse.RequestParser()
session_test_user_query_parser.add_argument('session_id', type=int, default=None)
session_test_user_query_parser.add_argument('test_id', type=int, default=None)
session_test_user_query_parser.add_argument('user_id', type=int, default=None)

@_resource('/errors')
class ErrorResource(ModelResource):

    MODEL = Error

    def _get_iterator(self):
        args = session_test_user_query_parser.parse_args()
        if args.session_id is not None:
            return Error.query.join((Session, Error.session)).filter(Session.id == args.session_id)
        elif args.test_id is not None:
            return Error.query.join((Test, Error.test)).filter(Test.id == args.test_id)
        abort(requests.codes.bad_request)


@_resource('/users', '/users/<object_id>')
class UserResource(ModelResource):

    ONLY_FIELDS = ['id', 'email']
    MODEL = User

    def _get_object_by_id(self, object_id):
        try:
            object_id = int(object_id)
        except ValueError:
            try:
                object_id = User.query.filter_by(email=object_id).one().id
            except NoResultFound:
                abort(requests.codes.not_found)
        return User.query.get_or_404(int(object_id))


@_resource('/comments', '/comments/<int:object_id>')
class CommentsResource(ModelResource):

    MODEL = Comment
    DEFAULT_SORT = (Comment.timestamp.asc(),)

    def _get_iterator(self):
        args = session_test_user_query_parser.parse_args()
        if args.session_id is not None:
            returned = Comment.query.join((Session, Comment.session)).filter(Session.id == args.session_id)
        elif args.test_id is not None:
            returned = Comment.query.join((Test, Comment.test)).filter(Test.id == args.test_id)
        else:
            abort(requests.codes.bad_request)
        return returned.join(User, Comment.user)

    def _paginate(self, iterator, metadata):
        return iterator


@_resource('/activities', '/activities/<int:object_id>')
class ActivityResource(ModelResource):

    MODEL = Activity
    DEFAULT_SORT = (Activity.timestamp.desc(),)

    def _get_iterator(self):
        returned = super(ActivityResource, self)._get_iterator()
        args = session_test_user_query_parser.parse_args()
        if args.session_id is not None:
            returned = returned.filter(Activity.session_id == args.session_id)
        if args.test_id is not None:
            returned = returned.filter(Activity.test_id == args.test_id)
        if args.user_id is not None:
            returned = returned.filter(Activity.user_id == args.user_id)
        return returned
