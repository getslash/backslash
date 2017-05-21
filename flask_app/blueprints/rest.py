# pylint: disable=no-member
import os

import requests

from flask import Blueprint, abort, request, jsonify, current_app, Response
from flask_restful import Api, reqparse
from sqlalchemy.orm.exc import NoResultFound

from flask_simple_api import error_abort
from flask_security import current_user

from .. import models
from ..models import Error, Session, Test, User, Subject
from .. import activity
from ..utils.identification import parse_test_id, parse_session_id
from ..utils.rest import ModelResource
from ..filters import filter_by_statuses
from ..search import get_orm_query_from_search_string

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
session_parser.add_argument('search', type=str, default=None)

@_resource('/sessions', '/sessions/<object_id>')
class SessionResource(ModelResource):

    MODEL = Session
    DEFAULT_SORT = (Session.start_time.desc(),)

    def _get_object_by_id(self, object_id):
        return _get_object_by_id_or_logical_id(self.MODEL, object_id)

    def _get_iterator(self):
        args = session_parser.parse_args()

        if args.search:
            returned = get_orm_query_from_search_string('session', args.search, abort_on_syntax_error=True)
        else:
            returned = super(SessionResource, self)._get_iterator()

        returned = returned.filter(Session.archived == False) # pylint: disable=singleton-comparison
        if args.subject_name is not None:
            returned = (
                returned
                .join(Session.subject_instances)
                .join(Subject)
                .filter(Subject.name == args.subject_name))

        if args.user_id is not None:
            returned = returned.filter(Session.user_id == args.user_id)

        returned = filter_by_statuses(returned, self.MODEL)

        return returned

test_query_parser = reqparse.RequestParser()
test_query_parser.add_argument('session_id', default=None)
test_query_parser.add_argument('info_id', type=int, default=None)
test_query_parser.add_argument('search', type=str, default=None)
test_query_parser.add_argument('after_index', type=int, default=None)
test_query_parser.add_argument('before_index', type=int, default=None)


@_resource('/tests', '/tests/<object_id>', '/sessions/<session_id>/tests')
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

        if args.search:
            returned = get_orm_query_from_search_string('test', args.search, abort_on_syntax_error=True)
        else:
            returned = super(TestResource, self)._get_iterator()

        if args.session_id is not None:
            try:
                session_id = int(args.session_id)
            except ValueError:
                returned = Test.query.join(Session).filter(Session.logical_id == args.session_id)
            else:
                returned = returned.filter(Test.session_id == session_id)

        if args.info_id is not None:
            returned = returned.filter(Test.test_info_id == args.info_id)

        returned = filter_by_statuses(returned, Test)

        if args.session_id is not None:
            if args.after_index is not None:
                returned = returned.filter(self.MODEL.test_index > args.after_index).order_by(self.MODEL.test_index.asc()).limit(1).all()
            elif args.before_index is not None:
                returned = returned.filter(self.MODEL.test_index < args.before_index).order_by(self.MODEL.test_index.desc()).limit(1).all()

        return returned


@_resource('/test_infos/<object_id>')
class TestInfoResource(ModelResource):

    MODEL = models.TestInformation


@_resource('/subjects', '/subjects/<object_id>')
class SubjectResource(ModelResource):

    MODEL = models.Subject
    ONLY_FIELDS = ['id', 'name', 'last_activity']
    SORTABLE_FIELDS = ['last_activity', 'name']
    INVERSE_SORTS = ['last_activity']

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

session_test_query_parser = reqparse.RequestParser()
session_test_query_parser.add_argument('session_id', type=int, default=None)
session_test_query_parser.add_argument('test_id', type=int, default=None)

errors_query_parser = reqparse.RequestParser()
errors_query_parser.add_argument('session_id', default=None)
errors_query_parser.add_argument('test_id', default=None)


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
        args = errors_query_parser.parse_args()

        if args.session_id is not None:
            return Error.query.filter_by(session_id=parse_session_id(args.session_id))
        elif args.test_id is not None:
            return Error.query.filter_by(test_id=parse_test_id(args.test_id))
        abort(requests.codes.bad_request)


@blueprint.route('/tracebacks/<uuid>')
def get_traceback(uuid):
    if not current_app.config['DEBUG'] and not current_app.config['TESTING']:
        abort(requests.codes.not_found)
    path = _get_traceback_path(uuid)
    if not os.path.isfile(path):
        abort(requests.codes.not_found)
    def sender():
        with open(path, 'rb') as f:
            while True:
                buff = f.read(4096)
                if not buff:
                    break
                yield buff
    return Response(sender(), headers={'Content-Encoding': 'gzip', 'Content-Type': 'application/json'})


def _get_traceback_path(uuid):
    return os.path.join(current_app.config['TRACEBACK_DIR'], uuid[:2], uuid + '.gz')


@_resource('/users', '/users/<object_id>')
class UserResource(ModelResource):

    ONLY_FIELDS = ['id', 'email', 'last_activity']
    SORTABLE_FIELDS = ['last_activity', 'email', 'first_name', 'last_name']
    INVERSE_SORTS = ['last_activity']
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

@_resource('/comments', '/comments/<object_id>', methods=['get', 'delete', 'put'])
class CommentResource(ModelResource):

    MODEL = models.Comment
    DEFAULT_SORT = (models.Comment.timestamp.asc(),)

    def _get_iterator(self):
        args = session_test_query_parser.parse_args()
        if not ((args.session_id is not None) ^ (args.test_id is not None)): # pylint: disable=superfluous-parens
            error_abort('Either test_id or session_id must be passed to the query')

        return models.Comment.query.filter_by(session_id=args.session_id, test_id=args.test_id)

    def delete(self, object_id=None):
        if object_id is None:
            error_abort('Not implemented', code=requests.codes.not_implemented)
        comment = models.Comment.query.get_or_404(object_id)
        if comment.session_id is not None:
            obj = models.Session.query.get(comment.session_id)
        else:
            obj = models.Test.query.get(comment.test_id)
        if comment.user_id != current_user.id:
            error_abort('Not allowed to delete comment', code=requests.codes.forbidden)
        obj.num_comments = type(obj).num_comments - 1
        models.db.session.add(obj)
        models.db.session.delete(comment)
        models.db.session.commit()

    def put(self, object_id=None):
        if object_id is None:
            error_abort('Not implemented', code=requests.codes.not_implemented)
        comment = models.Comment.query.get_or_404(object_id)
        if comment.user_id != current_user.id:
            error_abort('Not allowed to delete comment', code=requests.codes.forbidden)
        comment.comment = request.get_json().get('comment', {}).get('comment')
        comment.edited = True
        models.db.session.add(comment)
        models.db.session.commit()
        return jsonify({'comment': self._render_single(comment, in_collection=False)})


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
