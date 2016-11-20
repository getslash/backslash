class SearchException(Exception):
    pass

class SearchSyntaxError(SearchException):
    pass

class UnknownField(SearchSyntaxError):
    pass

class UnknownOperator(SearchSyntaxError):
    pass
