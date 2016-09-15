import operator

from .logic import get_current_logic, with_
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
}

alphanums_plus = alphanums + '_-/@.'
identifier = Word(alphanums_plus)
LPAR, RPAR = map(Suppress, '()')
QUOTE = Suppress('"')
func_call = Group(oneOf(list(_FUNCTIONS)) + LPAR + identifier + RPAR)
atom = func_call | identifier | (QUOTE + Word(alphanums_plus + ' ') + QUOTE)
binop = oneOf(list(_OPERATORS))

and_ = Keyword("and", caseless=True)
or_ = Keyword("or", caseless=True)


def _get_operator(opname):
    returned = _OPERATORS.get(opname)
    if returned is None:
        raise UnknownOperator(opname)
    return returned

grammar = infixNotation(atom, [
    (binop, 2, opAssoc.LEFT),
    (and_, 2, opAssoc.LEFT),
    (or_, 2, opAssoc.LEFT),
])


def transform_to_query(base_query, query_string):
    try:
        tokens = grammar.parseString(query_string, parseAll=True)
        _logger.trace('Got tokens: {}', tokens)
    except ParseException as e:
        raise SearchSyntaxError('Syntax error (line {}, col {}):\n{!r}\n{}^'.format(
            e.lineno, e.col, e.line, '~' * (e.col - 1))) from e

    return base_query.filter(_translate_tokens(tokens.asList()[0]))


def _translate_tokens(tokens):
    if len(tokens) == 2:
        func_name, operand = tokens
        return _FUNCTIONS[func_name](operand)

    if len(tokens) != 3:
        raise SearchSyntaxError('Invalid Syntax')
    lhs, op_name, rhs = tokens

    if op_name == 'and':
        return _translate_tokens(lhs) & _translate_tokens(rhs)
    if op_name == 'or':
        return _translate_tokens(lhs) | _translate_tokens(rhs)

    op = _get_operator(op_name)

    logic = get_current_logic()
    field = logic.resolve_model_field(lhs)
    rhs = logic.resolve_value(lhs, rhs)

    if field is None:
        raise UnknownField('Unknown field specified: {!r}'.format(lhs))

    if isinstance(field, ComputedSearchField):
        returned = field.get_query_expression(op, rhs)
        _logger.trace('{} {} {!r} ==> {}', lhs, op_name, rhs, returned)
        return returned

    return op(field, rhs)
