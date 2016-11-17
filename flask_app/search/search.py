import requests

from flask_simple_api import error_abort

from .logic import SearchContext
from .syntax import transform_to_query
from .exceptions import SearchSyntaxError

def get_orm_query_from_search_string(object_type, query, abort_on_syntax_error=False):
    with SearchContext.get_for_type(object_type) as ctx:
        base_query = ctx.get_base_query()

        try:
            returned = transform_to_query(base_query, query)
        except SearchSyntaxError:
            if not abort_on_syntax_error:
                raise
            error_abort('Syntax Error', code=requests.codes.bad_request)
        return returned

__all__ = ['get_orm_query_from_search_string']
