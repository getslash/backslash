# pylint: disable=no-member
import requests

from flask import Blueprint, abort, request, jsonify
from flask_restful import Api, reqparse
from sqlalchemy.orm.exc import NoResultFound

from flask.ext.simple_api import error_abort
from flask.ext.security import current_user

from .. import models
from ..models import Error, Session, Test, User, Subject
from .. import activity
from ..utils.rest import ModelResource

blueprint = Blueprint('rest', __name__, url_prefix='/rest')


rest = Api(blueprint)


def _resource(*args, **kwargs):
    def decorator(resource):
        rest.add_resource(resource, *args, **kwargs)
        return resource
    return decorator

##########################################################################

session_parser = reqparse.RequestParser()
session_parser.add_argument('user_id', type=int, default=None)
session_parser.add_argument('subject_name', type=str, default=None)

@_resource('/sessions', '/sessions/<object_id>')
class SessionResource(ModelResource):

    MODEL = Session
    DEFAULT_SORT = (Session.start_time.desc(),)
    from .filter_configs import SESSION_FILTERS as FILTER_CONFIG

    def _get_object_by_id(self, object_id):
        return _get_object_by_id_or_logical_id(self.MODEL, object_id)

    def _get_iterator(self):
        returned = super(SessionResource, self)._get_iterator()
        args = session_parser.parse_args()
        if args.subject_name is not None:
            returned = (
                returned
                .join(Session.subject_instances)
                .join(Subject)
                .filter(Subject.name == args.subject_name))

        if args.user_id is not None:
            returned = returned.filter(Session.user_id == args.user_id)

        return returned

test_query_parser = reqparse.RequestParser()
test_query_parser.add_argument('session_id', default=None)
test_query_parser.add_argument('info_id', type=int, default=None)


@_resource('/tests', '/tests/<object_id>', '/sessions/<int:session_id>/tests')
class TestResource(ModelResource):

    MODEL = Test
    DEFAULT_SORT = (Test.start_time.desc(),)
    from .filter_configs import TEST_FILTERS as FILTER_CONFIG

    def _get_object_by_id(self, object_id):
        return _get_object_by_id_or_logical_id(self.MODEL, object_id)

    def _get_iterator(self):
        args = test_query_parser.parse_args()

        if args.session_id is None:
            args.session_id = request.view_args.get('session_id')

        returned = super(TestResource, self)._get_iterator()

        if args.session_id is not None:
            try:
                session_id = int(args.session_id)
            except ValueError:
                return Test.query.join(Session).filter(Session.logical_id == args.session_id)

            returned = returned.filter(Test.session_id == session_id)

        if args.info_id is not None:
            returned = returned.filter(Test.test_info_id == args.info_id)

        return returned


@_resource('/test_infos/<object_id>')
class TestInfoResource(ModelResource):

    MODEL = models.TestInformation


@_resource('/subjects', '/subjects/<object_id>')
class SubjetInstanceResource(ModelResource):

    MODEL = models.Subject
    ONLY_FIELDS = ['id', 'name']

    def _get_object_by_id(self, object_id):
        try:
            object_id = int(object_id)
        except ValueError:
            try:
                return self.MODEL.query.filter(models.Subject.name == object_id).one()
            except NoResultFound:
                abort(requests.codes.not_found)
        else:
            return self.MODEL.query.get_or_404(object_id)


def _get_object_by_id_or_logical_id(model, object_id):
    query_filter = model.logical_id == object_id
    try:
        numeric_object_id = int(object_id)
    except ValueError:
        pass
    else:
        query_filter = (model.id == numeric_object_id) | query_filter
    returned = model.query.filter(query_filter).first()
    if returned is None:
        abort(requests.codes.not_found) # pylint: disable=no-member
    return returned


session_test_user_query_parser = reqparse.RequestParser()
session_test_user_query_parser.add_argument('session_id', type=int, default=None)
session_test_user_query_parser.add_argument('test_id', type=int, default=None)
session_test_user_query_parser.add_argument('user_id', type=int, default=None)


@_resource('/warnings', '/warnings/<int:object_id>')
class WarningsResource(ModelResource):

    MODEL = models.Warning
    DEFAULT_SORT = (models.Warning.timestamp.asc(),)

    def _get_iterator(self):
        args = session_test_user_query_parser.parse_args()
        returned = self.MODEL.query.filter_by(test_id=args.test_id, session_id=args.session_id)
        return returned


@_resource('/errors', '/errors/<int:object_id>')
class ErrorResource(ModelResource):

    MODEL = Error
    DEFAULT_SORT = (Error.timestamp.asc(),)

    def _get_iterator(self):
        args = session_test_user_query_parser.parse_args()

        if args.session_id is not None:
            return Error.query.filter_by(session_id=args.session_id)
        elif args.test_id is not None:
            return Error.query.filter_by(test_id=args.test_id)
        abort(requests.codes.bad_request)


@_resource('/users', '/users/<object_id>')
class UserResource(ModelResource):

    ONLY_FIELDS = ['id', 'email', 'last_activity']
    SORTABLE_FIELDS = ['last_activity', 'email']
    MODEL = User

    def _get_object_by_id(self, object_id):
        if object_id == 'self':
            if not current_user.is_authenticated:
                abort(requests.codes.not_found)
            object_id = current_user.id
        try:
            object_id = int(object_id)
        except ValueError:
            try:
                object_id = User.query.filter_by(email=object_id).one().id
            except NoResultFound:
                abort(requests.codes.not_found)
        return User.query.get_or_404(int(object_id))


@blueprint.route('/activities')
def get_activities():
    args = session_test_user_query_parser.parse_args()

    if not ((args.session_id is not None) ^
            (args.test_id is not None) ^
            (args.user_id is not None)):
        error_abort('Either test_id, session_id or user_id must be passed to the query')

    results = models.db.session.execute(
        activity.get_activity_query(user_id=args.user_id, test_id=args.test_id, session_id=args.session_id))

    return jsonify({
        'activities': [
            _fix_action_string(dict(obj.items())) for obj in results
        ]
    })

def _fix_action_string(d):
    d['action'] = activity.get_action_string(d['action'])
    return d
