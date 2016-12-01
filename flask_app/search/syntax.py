import functools
import operator

from .logic import get_current_logic, with_, without_
from .exceptions import UnknownField, UnknownOperator, SearchSyntaxError
from .computed_search_field import ComputedSearchField

from pyparsing import infixNotation, opAssoc, Word, alphanums, oneOf, Keyword, ParseException, Suppress, Group

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
    'with': with_,
    'without': without_,
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
    returned = _OPERATORS.get(opname)
    if returned is None:
        raise UnknownOperator(
            opname, reason='Unknown operator: {!r}'.format(opname))
    return returned


def _handle_func_call(s, l, tokens): # pylint: disable=unused-argument

    func_name, operand = tokens[0]
    return _FUNCTIONS[func_name](operand)


def _handle_binop(tokens):
    tokens = list(tokens)[0]

    if len(tokens) != 3:
        raise SearchSyntaxError('Invalid Syntax')

    lhs, op_name, rhs = tokens

    op = _get_operator(op_name)

    logic = get_current_logic()
    field = logic.resolve_model_field(lhs)
    rhs = logic.resolve_value(lhs, rhs)

    if field is None:
        raise UnknownField(
            'Unknown field', reason='Unknown field specified: {!r}'.format(lhs))

    if isinstance(field, ComputedSearchField):
        returned = field.get_query_expression(op, rhs)
        _logger.trace('{} {} {!r} ==> {}', lhs, op_name, rhs, returned)
        return returned

    return op(field, rhs)


def _handle_and(tokens):
    return functools.reduce(operator.and_, list(tokens)[0][::2])

def _handle_or(tokens):
    return functools.reduce(operator.or_, list(tokens)[0][::2])

alphanums_plus = alphanums + '_-/@.'
identifier = Word(alphanums_plus)
LPAR, RPAR = map(Suppress, '()')
QUOTE = Suppress('"')


func_call = Group(oneOf(list(_FUNCTIONS)) + LPAR + identifier + RPAR).setParseAction(_handle_func_call)


atom = func_call | identifier | (QUOTE + Word(alphanums_plus + ' ') + QUOTE)
binop = oneOf(list(_OPERATORS))

and_ = Keyword("and", caseless=True)
or_ = Keyword("or", caseless=True)


grammar = infixNotation(atom, [
    (binop, 2, opAssoc.LEFT, _handle_binop),
    (and_, 2, opAssoc.LEFT, _handle_and),
    (or_, 2, opAssoc.LEFT, _handle_or),
])
