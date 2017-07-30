import operator
from uuid import uuid4

import pytest

from flask_app import models
from flask_app.search import get_orm_query_from_search_string
from flask_app.search.logic import TestSearchContext
from flask_app.search.exceptions import SearchSyntaxError


def test_parsing_simple_exression():
    query = get_orm_query_from_search_string('test', 'name = test_blap')
    assert str(query) == str(TestSearchContext().get_base_query().filter(
        models.TestInformation.name == 'test_blap'))


@pytest.mark.parametrize('q', [
    'subject=obj123 and related=a.b.c.d and status != success',
    'name = bla and subject=subject',
    'start_time < "-2d"',
    'start_time < "2 days ago"',
    'start_time < "-2d"',
    'start_time < "12/1/2016"',
    'start_time = "26/11/2016 13:08:40"',
    "start_time = '26/11/2016 13:08:40'",
    'user=some_identifier and user=vmalloc@gmail.com',
    'label = testing',
    'label != testing',

])
def test_test_search(q):
    query = get_orm_query_from_search_string('test', q)
    _ = query.limit(5).all()


@pytest.mark.parametrize('q', [
    'related=related-entity1',
    'related=related-entity1',
    'related=obj123 and related=a.b.c.d',
    'related != bla and subject != bla',
    'product_version = 1.2.3',
])
@pytest.mark.parametrize('objtype', ['test', 'session'])
def test_related_subject_searches(objtype, q):
    query = get_orm_query_from_search_string(objtype, q)
    _ = query.limit(5).all()


@pytest.mark.parametrize('objtype', ['session', 'test'])
@pytest.mark.parametrize('negate', [True, False])
def test_subject_search(started_session, started_test, subjects, objtype, negate):
    started_session.add_subject(**subjects[0])
    query = get_orm_query_from_search_string(objtype, 'subject {} {}'.format('!=' if negate else '=', subjects[0].name)).limit(5)

    if negate:
        assert query.all()
    else:
        obj = query.one()
        assert obj.id == (started_session if objtype == 'session' else started_test).id


@pytest.mark.parametrize('q', [
    'start_time < "-2d"',
    'user = bla',
    'user != bla',
    'label = bla',
    'label != bla',
    'commandline = bla',
])
def test_session_search(q):
    query = get_orm_query_from_search_string('session', q)
    _ = query.limit(5).all()


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
    'start_time < dfdfd',
])
def test_invalid_syntax(q):
    with pytest.raises(SearchSyntaxError):
        get_orm_query_from_search_string('test', q)


@pytest.mark.parametrize('use_like', [True, False])
def test_computed_fields(ended_test, user_identifier, testuser_id, use_like):  # pylint: disable=unused-argument
    search_term = user_identifier[1:-1] if use_like else user_identifier

    tests = get_orm_query_from_search_string(
        'test', 'user {} {}'.format('~' if use_like else '=', search_term)).all()
    assert tests
    for t in tests:
        assert t.session.user.id == testuser_id


@pytest.fixture(params=[
    operator.attrgetter('first_name'),
    operator.attrgetter('last_name'),
    operator.attrgetter('email'),
])
def user_identifier(request, testuser_id, active_db_context):  # pylint: disable=unused-argument
    testuser = models.User.query.get(testuser_id)
    return request.param(testuser)


@pytest.fixture(autouse=True)
def db_context_active(active_db_context):  # pylint: disable=unused-argument
    pass


@pytest.fixture(autouse=True)
def testuser_with_full_name(testuser_id, active_db_context):  # pylint: disable=unused-argument
    testuser = models.User.query.get(testuser_id)
    testuser.first_name = str(uuid4())
    testuser.last_name = str(uuid4())
    models.db.session.add(testuser)
    models.db.session.commit()
