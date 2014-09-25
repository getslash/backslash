import pytest


def test_search_by_test_name(client, test_to_find_name, test_name):
    [test] = client.query_tests().filter(name=test_name)
    assert test == test_to_find_name


def test_search_by_test_logical_id(client, test_to_find_logical_id, logical_id):
    [test] = client.query_tests().filter(logical_id=logical_id)
    assert test == test_to_find_logical_id


def test_search_by_status_success(client, test_to_find_status_success):
    [test] = client.query_tests().filter(status='SUCCESS')
    assert test == test_to_find_status_success


def test_search_by_status_running(client, test_to_find_status_running):
    [test] = client.query_tests().filter(status='RUNNING')
    assert test == test_to_find_status_running


def test_search_by_status_failure(client, test_to_find_status_failure):
    [test] = client.query_tests().filter(status='FAILURE')
    assert test == test_to_find_status_failure


def test_search_by_status_error(client, test_to_find_status_error):
    [test] = client.query_tests().filter(status='ERROR')
    assert test == test_to_find_status_error


def test_search_by_status_skipped(client, test_to_find_status_skipped):
    [test] = client.query_tests().filter(status='SKIPPED')
    assert test == test_to_find_status_skipped


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


@pytest.fixture
def test_to_find_status_success(started_session):
    test = started_session.report_test_start()
    test.report_end()
    test.refresh()
    return test


@pytest.fixture
def test_to_find_status_error(started_session):
    test = started_session.report_test_start()
    test.add_error()
    test.report_end()
    test.refresh()
    return test


@pytest.fixture
def test_to_find_status_skipped(started_session):
    test = started_session.report_test_start()
    test.report_end(skipped=True)
    test.refresh()
    return test


@pytest.fixture
def test_to_find_status_failure(started_session):
    test = started_session.report_test_start()
    test.add_failure()
    test.report_end()
    test.refresh()
    return test


@pytest.fixture
def test_to_find_status_running(started_session):
    test = started_session.report_test_start()
    test.refresh()
    return test



