class ComputedSearchField(object):

    def get_query_expression(self, op, field_value):
        raise NotImplementedError() # pragma: no cover


class Either(ComputedSearchField):

    def __init__(self, fields):
        super(Either, self).__init__()
        self.fields = fields

    def get_query_expression(self, op, field_value):
        returned = op(self.fields[0], field_value)
        for f in self.fields[1:]:
            returned |= op(f, field_value)
        return returned
