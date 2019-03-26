# pylint: disable=no-member
import math
import os

import requests

from flask import Blueprint, abort, request, jsonify, current_app, Response
from flask_restful import Api, reqparse
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func, or_
from sqlalchemy.orm import aliased

from flask_simple_api import error_abort
from flask_security import current_user
from .. import models
from ..models import Error, Session, Test, User, Subject, db, UserStarredTests
from .. import activity
from ..utils.identification import parse_test_id, parse_session_id
from ..utils.users import has_role
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
session_parser.add_argument('parent_logical_id', type=str, default=None)
session_parser.add_argument('id', type=str, default=None)

@_resource('/sessions', '/sessions/<object_id>')
class SessionResource(ModelResource):

    MODEL = Session
    DEFAULT_SORT = (Session.start_time.desc(),)

    def _get_object_by_id(self, object_id):
        return _get_object_by_id_or_logical_id(self.MODEL, object_id)

    def _get_iterator(self):
        args = session_parser.parse_args()

        if args.id is not None:
            return _get_query_by_id_or_logical_id(self.MODEL, args.id)
        if args.search:
            returned = get_orm_query_from_search_string('session', args.search, abort_on_syntax_error=True)
        else:
            returned = super(SessionResource, self)._get_iterator()

        if args.parent_logical_id is not None:
            returned =  returned.filter(Session.parent_logical_id == args.parent_logical_id)
        else:
            returned = returned.filter(Session.parent_logical_id == None)
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
test_query_parser.add_argument('id', type=str, default=None)
test_query_parser.add_argument('starred', type=bool, default=False)
test_query_parser.add_argument('user_id', type=int, default=None)

@_resource('/tests', '/tests/<object_id>', '/sessions/<session_id>/tests')
class TestResource(ModelResource):

    MODEL = Test
    DEFAULT_SORT = (Test.start_time.desc(),)
    from .filter_configs import TEST_FILTERS as FILTER_CONFIG

    def _get_object_by_id(self, object_id):
        return _get_object_by_id_or_logical_id(self.MODEL, object_id)

    def _render_many(self, objects, *, in_collection: bool):
        args = test_query_parser.parse_args()
        user_id = args.user_id or getattr(current_user, 'id', None)
        rendered_tests = super()._render_many(objects, in_collection=in_collection)
        if not rendered_tests or not current_user.is_authenticated:
            return rendered_tests
        if not in_collection:
            rendered_tests['is_starred'] = db.session.query(db.session.query(UserStarredTests).filter(UserStarredTests.user_id == user_id, UserStarredTests.test_id==rendered_tests['id']).exists()).scalar()
        else:
            rendered_test_ids = [test['id'] for test in rendered_tests['tests']]
            starred_test_ids = set([test_id for (test_id, ) in db.session.query(Test.id).join(UserStarredTests).filter(UserStarredTests.user_id == user_id, Test.id.in_(rendered_test_ids)).all()])
            for test in rendered_tests['tests']:
                test['is_starred'] = test['id'] in starred_test_ids
        return rendered_tests

    def _get_iterator(self):
        args = test_query_parser.parse_args()
        user_id = user_id = args.user_id or getattr(current_user, 'id', None)
        if args.id is not None:
            return _get_query_by_id_or_logical_id(self.MODEL, args.id)
        if args.starred:
            return Test.query.join(UserStarredTests).filter(UserStarredTests.user_id == user_id).order_by(UserStarredTests.star_creation_time.desc()).all()
        if args.session_id is None:
            args.session_id = request.view_args.get('session_id')

        if args.search:
            returned = get_orm_query_from_search_string('test', args.search, abort_on_syntax_error=True)
        else:
            returned = super(TestResource, self)._get_iterator().join(Session, Session.id == Test.session_id)


        # get session
        if args.session_id is not None:
            returned = self._filter_by_session_id(returned, args.session_id)

        if args.info_id is not None:
            returned = returned.filter(Test.test_info_id == args.info_id)

        returned = filter_by_statuses(returned, Test)

        if args.session_id is not None:
            if args.after_index is not None:
                returned = returned.filter(self.MODEL.test_index > args.after_index).order_by(self.MODEL.test_index.asc()).limit(1).all()
            elif args.before_index is not None:
                returned = returned.filter(self.MODEL.test_index < args.before_index).order_by(self.MODEL.test_index.desc()).limit(1).all()

        return returned

    def _filter_by_session_id(self, query, session_id):
        try:
            int(session_id)
        except ValueError:
            id_field = lambda model: model.logical_id
        else:
            id_field = lambda model: model.id

        session_aliased = aliased(Session)
        children = (
            db.session.query(id_field(Session))
            .filter(
                db.session.query(session_aliased.id)
                .filter(id_field(session_aliased) == session_id)
                .filter(session_aliased.logical_id == Session.parent_logical_id)
                .exists()
            )
            .all()
        )
        children_ids = [row[0] for row in children]
        criterion = id_field(Session) == session_id
        if children_ids:
            criterion |= id_field(Session).in_(children_ids)
        returned = query.filter(criterion)
        return returned

    def _paginate(self, query, metadata):
        count_pages = bool(request.args.get('session_id'))
        if count_pages:
            num_objects = query.count()
        else:
            num_objects = None
        returned = super()._paginate(query, metadata)
        if count_pages:
            metadata['num_pages'] = math.ceil(num_objects / metadata['page_size']) or 1
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


def _get_query_by_id_or_logical_id(model, object_id):
    query_filter = model.logical_id == object_id
    try:
        numeric_object_id = int(object_id)
    except ValueError:
        pass
    else:
        query_filter = (model.id == numeric_object_id) | query_filter
    return model.query.filter(query_filter)

def _get_object_by_id_or_logical_id(model, object_id):
    returned = _get_query_by_id_or_logical_id(model, object_id).first()
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
errors_query_parser.add_argument('interruptions', default=False, type=bool)


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
            session = _get_object_by_id_or_logical_id(Session, args.session_id)
            # We want to query only the session's own errors if it is either a non-parllel session or a child session
            if session.parent_logical_id is not None or not session.is_parent_session:
                query = db.session.query(Error).filter(Error.session_id == session.id)
            else:
                query = db.session.query(Error).join(Session).filter(or_(Session.id == session.id, Session.parent_logical_id == session.logical_id))

        elif args.test_id is not None:
            query = Error.query.filter_by(test_id=parse_test_id(args.test_id))
        else:
            abort(requests.codes.bad_request)

        if args.interruptions:
            query = query.filter_by(is_interruption=True)
        else:
            query = query.filter((self.MODEL.is_interruption == False) | (self.MODEL.is_interruption == None)) # pylint: disable=singleton-comparison
        return query


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

    def _get_iterator(self):
        returned = super()._get_iterator()
        if request.args.get('current_user'):
            if not current_user.is_authenticated:
                return []
            object_id = current_user.id
            returned = returned.filter(self.MODEL.id == object_id)

        filter = request.args.get('filter')
        if filter:
            filter = filter.lower()
            returned = returned.filter(func.lower(User.first_name).contains(filter) | func.lower(User.last_name).contains(filter) | func.lower(User.email).contains(filter))
        return returned

    def _get_object_by_id(self, object_id):
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


related_entity_parser = reqparse.RequestParser()
related_entity_parser.add_argument('session_id', default=None, type=int)
related_entity_parser.add_argument('test_id', default=None, type=int)


@_resource('/entities', '/entities/<int:object_id>')
class RelatedEntityResource(ModelResource):

    MODEL = models.Entity

    def _get_iterator(self):
        args = related_entity_parser.parse_args()

        if not ((args.session_id is None) ^ (args.test_id is None)):
            error_abort('Either test_id or session_id must be provided')

        if args.session_id is not None:
            return models.Entity.query.join(models.session_entity).filter(models.session_entity.c.session_id == args.session_id)
        elif args.test_id is not None:
            return models.Entity.query.join(models.test_entity).filter(models.test_entity.c.test_id == args.test_id)
        else:
            raise NotImplementedError() # pragma: no cover


@_resource('/migrations', '/migrations/<object_id>')
class MigrationsResource(ModelResource):

    MODEL = models.BackgroundMigration
    DEFAULT_SORT = (models.BackgroundMigration.started_time.desc(),)
    ONLY_FIELDS = [
        'id',
        'name',
        'started',
        'started_time',
        'finished',
        'finished_time',
        'total_num_objects',
        'remaining_num_objects'
    ]


@_resource('/cases', '/cases/<object_id>')
class CaseResource(ModelResource):

    MODEL = models.TestInformation
    DEFAULT_SORT = (models.TestInformation.name, models.TestInformation.file_name, models.TestInformation.class_name)

    def _get_iterator(self):
        search = request.args.get('search')
        if search:
            returned = get_orm_query_from_search_string('case', search, abort_on_syntax_error=True)
        else:
            returned = super()._get_iterator()
        returned = returned.filter(~self.MODEL.file_name.like('/%'))
        return returned


@_resource('/replications', '/replications/<object_id>')
class ReplicationsResource(ModelResource):

    MODEL = models.Replication
    ONLY_FIELDS = [
        'id',
        'paused',
        'avg_per_second',
        'backlog_remaining',
        'last_replicated_timestamp',
        'last_error',
        'service_type',
        'username',
        'url'
    ]

    def _render_many(self, objects, *, in_collection: bool):
        returned = super()._render_many(objects, in_collection=in_collection)
        [latest_timestamp] = models.db.session.query(func.max(models.Test.updated_at)).one()

        if latest_timestamp:
            latest_timestamp = latest_timestamp.timestamp()

        if in_collection:
            collection = returned['replications']
        else:
            collection = [returned]

        for replication in collection:
            last_replicated = replication['last_replicated_timestamp']
            if not latest_timestamp or not last_replicated:
                lag = None
            else:
                lag = latest_timestamp - last_replicated
            replication['lag_seconds'] = lag

        return returned

    def put(self, object_id=None):
        if object_id is None:
            error_abort('Not implemented', code=requests.codes.not_implemented)
        if not has_role(current_user, 'admin'):
            error_abort('Forbidden', code=requests.codes.forbidden)
        replication = models.Replication.query.get_or_404(object_id)
        request_json = request.get_json().get("replication", {})
        for field_name in {'username', 'url', 'password'}:
            value = request_json.get(field_name)
            if value is not None:
                setattr(replication, field_name, value)
        models.db.session.commit()
        return jsonify({'replication': self._render_single(replication, in_collection=False)})


@blueprint.route('/admin_alerts')
def get_admin_alerts():
    return jsonify({
        'admin_alerts': [
            {
                'id': index,
                "message": alert,
            }
            for index, alert in enumerate(_iter_alerts(), 1)
        ]
    })

def _iter_alerts():
    if models.Replication.query.filter(models.Replication.last_error != None).count():
        yield "Some data replication services experienced errors"
