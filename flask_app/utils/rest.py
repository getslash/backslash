import logbook
from flask import jsonify, request

from flask_restful import reqparse, Resource
from sqlalchemy.orm import class_mapper
from sqlalchemy import text

from .rendering import render_api_object
from .english import plural_noun

_logger = logbook.Logger(__name__)


class RestResource(Resource):

    def get(self, **kw):
        object_id = request.view_args.get('object_id')
        if object_id is not None:
            _logger.debug('Looking for object id {}', object_id)
            obj = self._get_object_by_id(object_id)
            return self._format_result({self._get_single_object_key(): self._render_single(obj)})
        else:
            returned = self._paginate(self._get_iterator())
            result = {}
            for obj in returned:
                key = self._get_collection_key_for_object(obj)
                collection = result.get(key)
                if collection is None:
                    collection = result[key] = []
                collection.append(self._render_single(obj))
            return self._format_result(result)

    def _get_object_by_id(self, object_id):
        raise NotImplementedError()  # pragma: no cover

    def _get_iterator(self):
        raise NotImplementedError()  # pragma: no cover

    def _paginate(self, iterator):
        raise NotImplementedError()  # pragma: no cover

    def _get_collection_key_for_object(self, obj):
        raise NotImplementedError()  # pragma: no cover

    def _get_single_object_key(self):
        raise NotImplementedError() # pragma: no cover

    def _render_single(self, obj):
        raise NotImplementedError()  # pragma: no cover

    def _format_result(self, result):
        return jsonify(result)


class ModelResource(RestResource):

    MODEL = None
    ONLY_FIELDS = None
    DEFAULT_SORT = None

    def _get_iterator(self):
        assert self.MODEL is not None
        returned = self.MODEL.query
        if self.DEFAULT_SORT is not None:
            returned = returned.order_by(text(self.DEFAULT_SORT))
        return returned

    def _get_object_by_id(self, object_id):
        assert self.MODEL is not None
        return self.MODEL.query.get(object_id)

    def _render_single(self, obj):
        return render_api_object(obj, only_fields=self.ONLY_FIELDS)

    def _paginate(self, query):
        args = pagination_parser.parse_args()
        return query.offset((args.page - 1) * args.page_size).limit(args.page_size)

    def _get_collection_key_for_object(self, obj):
        return plural_noun(get_model_typename(type(obj)))

    def _get_single_object_key(self):
        return get_model_typename(self.MODEL)

    def _format_result(self, result):
        if not result:
            result[plural_noun(get_model_typename(self.MODEL))] = []
        return super(ModelResource, self)._format_result(result)


pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument(
    'page_size', type=int, location='args', default=30)
pagination_parser.add_argument('page', type=int, location='args', default=1)


def get_model_typename(model):
    assert isinstance(model, type)
    return model.__name__.lower()
