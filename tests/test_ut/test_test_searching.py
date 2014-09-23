import pytest


def test_search_by_test_name(client, test_to_find_name, test_name):
    [test] = client.query_tests().filter(name=test_name)
    assert test == test_to_find_name


def test_search_by_test_logical_id(client, test_to_find_logical_id, logical_id):
    [test] = client.query_tests().filter(logical_id=logical_id)
    assert test == test_to_find_logical_id


@pytest.fixture
def test_to_find_name(started_session, test_name):
    test = started_session.report_test_start(name=test_name)
    test.report_end()
    started_session.report_end()
    test.refresh()
    return test


@pytest.fixture
def test_to_find_logical_id(started_session, logical_id):
    test = started_session.report_test_start(test_logical_id=logical_id)
    test.report_end()
    started_session.report_end()
    test.refresh()
    return test

