from flask import jsonify

from flask_restful import reqparse, Resource
from weber_utils.request_utils import dictify_model


class RestResource(Resource):

    def get(self):
        returned = self._paginate(self._get_iterator())
        result = {}
        for obj in returned:
            key = self._get_key(obj)
            collection = result.get(key)
            if collection is None:
                collection = result[key] = []
            collection.append(self._render_single(obj))
        return self._format_result(result)

    def _get_iterator(self):
        raise NotImplementedError() # pragma: no cover

    def _paginate(self, iterator):
        raise NotImplementedError() # pragma: no cover

    def _get_key(self, objtype):
        return objtype.__class__.__name__.lower()

    def _render_single(self, obj):
        return dictify_model(obj)

    def _format_result(self, result):
        return jsonify(result)

class ModelResource(RestResource):

    MODEL = None

    def _get_iterator(self):
        assert self.MODEL is not None
        return self.MODEL.query

    def _paginate(self, query):
        args = pagination_parser.parse_args()
        return query.offset((args.page - 1) * args.page_size).limit(args.page_size)



pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page_size', type=int, location='args', default=30)
pagination_parser.add_argument('page', type=int, location='args', default=1)

