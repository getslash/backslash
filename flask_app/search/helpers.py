import functools

from .exceptions import UnknownOperator

def only_ops(ops):

    def decorator(func):
        @functools.wraps(func)
        def new_func(self, op, value):
            if op.op not in ops:
                raise UnknownOperator(op.op)
            return func(self, op, value)
        return new_func
    return decorator
