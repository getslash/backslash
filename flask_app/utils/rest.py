import math
import logbook
from flask import jsonify, request

from flask_restful import reqparse, Resource
from sqlalchemy.orm import class_mapper
from sqlalchemy import text

from .rendering import render_api_object
from .english import plural_noun
_logger = logbook.Logger(__name__)


class RestResource(Resource):

    FILTER_CONFIG = None

    def get(self, **kw):
        object_id = request.view_args.get('object_id')
        metadata = {}
        if object_id is not None:
            _logger.debug('Looking for object id {}', object_id)
            obj = self._get_object_by_id(object_id)
            return self._format_result({self._get_single_object_key(): self._render_single(obj)}, metadata=metadata)
        else:
            iterator = self._get_iterator()
            iterator = self._filter(iterator, metadata)
            iterator = self._sort(iterator, metadata)
            returned = self._paginate(iterator, metadata)
            result = {}
            for obj in returned:
                key = self._get_collection_key_for_object(obj)
                collection = result.get(key)
                if collection is None:
                    collection = result[key] = []
                collection.append(self._render_single(obj))
            return self._format_result(result, metadata=metadata)

    def _filter(self, iterator, metadata):
        if self.FILTER_CONFIG is None:
            return iterator
        return self.FILTER_CONFIG.filter(iterator, metadata)

    def _sort(self, iterator, metadata):
        return iterator

    def _get_object_by_id(self, object_id):
        raise NotImplementedError()  # pragma: no cover

    def _get_iterator(self):
        raise NotImplementedError()  # pragma: no cover

    def _paginate(self, iterator, metadata):
        raise NotImplementedError()  # pragma: no cover

    def _get_collection_key_for_object(self, obj):
        raise NotImplementedError()  # pragma: no cover

    def _get_single_object_key(self):
        raise NotImplementedError() # pragma: no cover

    def _render_single(self, obj):
        raise NotImplementedError()  # pragma: no cover

    def _format_result(self, result, metadata=None):
        result['meta'] = metadata or {}
        return jsonify(result)


class ModelResource(RestResource):

    MODEL = None
    ONLY_FIELDS = None
    EXTRA_FIELDS = None
    DEFAULT_SORT = None

    def _get_iterator(self):
        assert self.MODEL is not None
        returned = self.MODEL.query
        return returned

    def _get_object_by_id(self, object_id):
        assert self.MODEL is not None
        return self.MODEL.query.get(object_id)

    def _render_single(self, obj):
        return render_api_object(obj, only_fields=self.ONLY_FIELDS, extra_fields=self.EXTRA_FIELDS)

    def _sort(self, iterator, metadata):
        if self.DEFAULT_SORT is not None:
            iterator = iterator.order_by(*self.DEFAULT_SORT)
        return iterator

    def _paginate(self, query, metadata):
        args = pagination_parser.parse_args()
        metadata['total'] = query.count()
        metadata['pages_total'] = int(math.ceil(metadata['total'] / args.page_size)) or 1
        metadata['page'] = args.page
        metadata['page_size'] = args.page_size
        return query.offset((args.page - 1) * args.page_size).limit(args.page_size)

    def _get_collection_key_for_object(self, obj):
        return plural_noun(obj.get_typename())

    def _get_single_object_key(self):
        return self.MODEL.get_typename()

    def _format_result(self, result, metadata):
        if not result:
            result[plural_noun(get_model_typename(self.MODEL))] = []
        return super(ModelResource, self)._format_result(result, metadata)


pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument(
    'page_size', type=int, location='args', default=10)
pagination_parser.add_argument('page', type=int, location='args', default=1)

