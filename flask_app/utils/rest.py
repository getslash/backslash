import math
import logbook
from flask import jsonify, request, current_app

from flask_restful import reqparse, Resource
from flask.ext.simple_api import error_abort

from .rendering import render_api_object
from .english import plural_noun
_logger = logbook.Logger(__name__)


class RestResource(Resource):

    FILTER_CONFIG = None

    def get(self, **_):
        object_id = request.view_args.get('object_id')
        metadata = {}
        if object_id is not None:
            obj = self._get_object_by_id(object_id)
            return self._format_result({self._get_single_object_key(): self._render_single(obj, in_collection=False)}, metadata=metadata)
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
                collection.append(self._render_single(obj, in_collection=True))
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

    def _render_single(self, obj, *, in_collection: bool):
        raise NotImplementedError()  # pragma: no cover

    def _format_result(self, result, metadata=None):
        result['meta'] = metadata or {}
        return jsonify(result)


class ModelResource(RestResource):

    MODEL = None
    ONLY_FIELDS = None
    EXTRA_FIELDS = None
    DEFAULT_SORT = None
    SORTABLE_FIELDS = []

    def _get_iterator(self):
        assert self.MODEL is not None
        returned = self.MODEL.query
        return returned

    def _get_object_by_id(self, object_id):
        assert self.MODEL is not None
        return self.MODEL.query.get(object_id)

    def _render_single(self, obj, *, in_collection: bool):
        return render_api_object(obj, only_fields=self.ONLY_FIELDS, extra_fields=self.EXTRA_FIELDS, is_single=not in_collection)

    def _sort(self, iterator, metadata):
        sort_fields_expr = request.args.get('sort', None)
        if sort_fields_expr:
            sort_fields = []
            for sort_field in sort_fields_expr.split(','):
                desc = sort_field.startswith('-')
                if desc:
                    sort_field = sort_field[1:]
                sort_fields.append((not desc, sort_field))
            if not all((sort_field in self.SORTABLE_FIELDS) for _, sort_field in sort_fields):
                error_abort('Cannot sort according to given criteria - can only sort by {}'.format(', '.join(self.SORTABLE_FIELDS)))


            iterator = iterator.order_by(*[self._build_sort_expr(self.MODEL, f, asc) for asc, f in sort_fields])
        elif self.DEFAULT_SORT is not None:
            iterator = iterator.order_by(*self.DEFAULT_SORT) # pylint: disable=not-an-iterable
        return iterator

    def _build_sort_expr(self, model, field_name, asc):
        returned = getattr(model, field_name)
        if asc:
            returned = returned.asc()
        else:
            returned = returned.desc()
        return returned

    def _paginate(self, query, metadata):
        args = pagination_parser.parse_args()
        page_size = metadata['page_size'] = args.page_size
        max_page_size = current_app.config['MAX_QUERY_PAGE_SIZE']
        if page_size > max_page_size:
            error_abort('Query attempted to fetch more than the maximum number of results per page ({})'.format(max_page_size))

        metadata['total'] = query.count()
        metadata['pages_total'] = int(math.ceil(metadata['total'] / args.page_size)) or 1
        metadata['page'] = args.page
        return query.offset((args.page - 1) * args.page_size).limit(args.page_size)

    def _get_collection_key_for_object(self, obj):
        return plural_noun(obj.get_typename())

    def _get_single_object_key(self):
        return self.MODEL.get_typename()

    def _format_result(self, result, metadata):
        if not result:
            result[plural_noun(self.MODEL.get_typename())] = []
        return super(ModelResource, self)._format_result(result, metadata)


pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument(
    'page_size', type=int, location='args', default=10)
pagination_parser.add_argument('page', type=int, location='args', default=1)
