import functools
import operator

from .logic import get_current_logic
from .exceptions import UnknownField, UnknownOperator, SearchSyntaxError

from pyparsing import infixNotation, opAssoc, Word, alphanums, oneOf, Keyword, ParseException, Suppress, Group

import sqlalchemy
from sqlalchemy.sql.elements import BinaryExpression, UnaryExpression

import logbook

_logger = logbook.Logger(__name__)


_OPERATORS = {
    '~': lambda field, term: field.contains(term),
    '=': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge,
}

_FUNCTIONS = {
}


def transform_to_query(base_query, query_string):
    try:
        tokens = grammar.parseString(query_string, parseAll=True)
    except ParseException as e:
        raise SearchSyntaxError('Syntax error (line {}, col {}):\n{!r}\n{}^'.format(
            e.lineno, e.col, e.line, '~' * (e.col - 1))) from e

    query = list(tokens)[0]

    if isinstance(query, str):
        query = get_current_logic().get_fallback_filter(query)

    return base_query.filter(query)


def _get_operator(opname):
    func = _OPERATORS.get(opname)
    if func is None:
        raise UnknownOperator(
            opname, reason='Unknown operator: {!r}'.format(opname))
    return Operator(op=opname, func=func)


class Operator(object):

    def __init__(self, op, func):
        super().__init__()
        self.op = op
        self.func = func


def _handle_func_call(s, l, tokens):  # pylint: disable=unused-argument

    func_name, operand = tokens[0]
    return _FUNCTIONS[func_name](operand)


def _handle_binop(tokens):
    tokens = list(tokens)[0]

    if len(tokens) != 3:
        raise SearchSyntaxError('Invalid Syntax')

    lhs, op_name, rhs = tokens

    op = _get_operator(op_name)

    logic = get_current_logic()

    return logic.resolve_search_clause(lhs, op, rhs)


def _handle_and(tokens):
    return functools.reduce(sqlalchemy.and_, [_handle_logical_argument(arg) for arg in list(tokens)[0][::2]])


def _handle_or(tokens):
    return functools.reduce(sqlalchemy.or_, [_handle_logical_argument(arg) for arg in list(tokens)[0][::2]])

def _handle_logical_argument(arg):
    if not isinstance(arg, (BinaryExpression, UnaryExpression, bool)):
        assert isinstance(arg, str)
        arg = get_current_logic().get_fallback_filter(arg)
    return arg

alphanums_plus = alphanums + '_-/@.:'
identifier = Word(alphanums_plus)
LPAR, RPAR = map(Suppress, '()')
DQUOTE = Suppress('"')
SQUOTE = Suppress("'")


func_call = Group(oneOf(list(_FUNCTIONS)) + LPAR +
                  identifier + RPAR).setParseAction(_handle_func_call)


atom = func_call | identifier | (DQUOTE + Word(alphanums_plus + ' ') + DQUOTE) | (SQUOTE + Word(alphanums_plus + ' ') + SQUOTE)
binop = oneOf(list(_OPERATORS))

and_ = Keyword("and", caseless=True)
or_ = Keyword("or", caseless=True)


grammar = infixNotation(atom, [
    (binop, 2, opAssoc.LEFT, _handle_binop),
    (and_, 2, opAssoc.LEFT, _handle_and),
    (or_, 2, opAssoc.LEFT, _handle_or),
])
