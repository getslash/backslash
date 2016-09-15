import datetime
import operator
from uuid import uuid4

import pytest

from flask_app import models
from flask_app.search import get_orm_query_from_search_string
from flask_app.search.logic import TestSearchContext
from flask_app.search.value_parsers import parse_date
from flask_app.search.exceptions import SearchSyntaxError


def test_parsing_simple_exression():
    query = get_orm_query_from_search_string('test', 'name = test_blap')
    assert str(query) == str(TestSearchContext().get_base_query().filter(
        models.TestInformation.name == 'test_blap'))

@pytest.mark.parametrize('q', [
    'with(related-entity1)',
    'name = bla and with(subject)',
    'start_time < "-2d"',
    'start_time < "2 days ago"',
    'start_time < "-2d"',
    'start_time < "12/1/2016"',
    ])
def test_search_functions(q):
    _ = get_orm_query_from_search_string('test', q)

@pytest.mark.parametrize('date', [
    '-2d',
    '2 days ago',
    '12/1/2016',
    ])
def test_date_parser(date):
    assert isinstance(parse_date(date), datetime.datetime)


@pytest.mark.parametrize('q', [
    'name = {} and id = {}',
    '(name = {}) and id = {}',
    'name = {} and (id = {})',
])
def test_parsing_and_or_exression(q, ended_test):
    q = q.format(ended_test.info['name'], ended_test.id)
    _ = get_orm_query_from_search_string('test', q)


@pytest.mark.parametrize('q', [
    'name = ffff|||',
    'fff',
    'fdfd',
    'start_time < dfdfd',
])
def test_invalid_syntax(q):
    with pytest.raises(SearchSyntaxError):
        get_orm_query_from_search_string('test', q)


@pytest.mark.parametrize('use_like', [True, False])
def test_computed_fields(ended_test, user_identifier, testuser_id, use_like): # pylint: disable=unused-argument
    search_term = user_identifier[1:-1] if use_like else user_identifier

    tests = get_orm_query_from_search_string('test', 'user {} {}'.format('~' if use_like else '=', search_term)).all()
    assert tests
    for t in tests:
        assert t.session.user.id == testuser_id


@pytest.fixture(params=[
    operator.attrgetter('first_name'),
    operator.attrgetter('last_name'),
    operator.attrgetter('email'),
])
def user_identifier(request, testuser_id, active_db_context): # pylint: disable=unused-argument
    testuser = models.User.query.get(testuser_id)
    return request.param(testuser)


@pytest.fixture(autouse=True)
def db_context_active(active_db_context):  # pylint: disable=unused-argument
    pass

@pytest.fixture(autouse=True)
def testuser_with_full_name(testuser_id, active_db_context): # pylint: disable=unused-argument
    testuser = models.User.query.get(testuser_id)
    testuser.first_name = str(uuid4())
    testuser.last_name = str(uuid4())
    models.db.session.add(testuser)
    models.db.session.commit()
