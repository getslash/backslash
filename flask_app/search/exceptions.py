class SearchException(Exception):
    pass

class SearchSyntaxError(SearchException):

    def __init__(self, msg, reason='Syntax error'):
        super(SearchSyntaxError, self).__init__(msg)
        self.reason = reason

class UnknownField(SearchSyntaxError):
    pass

class UnknownOperator(SearchSyntaxError):
    pass
