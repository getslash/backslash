import pytest
from .utils import raises_bad_request


def test_search_by_test_name(client, test_to_find_name, test_name):
    [test] = client.query_tests().filter(name=test_name)
    assert test == test_to_find_name


def test_search_by_test_logical_id(client, test_to_find_logical_id, logical_id):
    [test] = client.query_tests().filter(logical_id=logical_id)
    assert test == test_to_find_logical_id


def test_search_by_bad_status(client):
    with raises_bad_request():
        #because of lazy evaluation we need to assign and "use" the result
        [dontcare] = client.query_tests().filter(status='BADSTATUS')


def test_search_by_status_success(client, test_to_find_status_success):
    [test] = client.query_tests().filter(status='SUCCESS')
    assert test == test_to_find_status_success


@pytest.mark.parametrize('new_status', ['RUNNING', 'SKIPPED', 'FAILURE', 'ERROR', 'INTERRUPTED'])
def test_search_by_status_success_modified(client, test_to_find_status_success, new_status):
    test_to_find_status_success.edit_status(new_status)
    test_to_find_status_success.refresh()
    success_tests = client.query_tests().filter(status='SUCCESS')
    assert len(success_tests) == 0
    [test] = client.query_tests().filter(status=new_status)
    assert test == test_to_find_status_success


def test_search_by_status_running(client, test_to_find_status_running):
    [test] = client.query_tests().filter(status='RUNNING')
    assert test == test_to_find_status_running


@pytest.mark.parametrize('new_status', ['SUCCESS', 'SKIPPED', 'FAILURE', 'ERROR', 'INTERRUPTED'])
def test_search_by_status_running_modified(client, test_to_find_status_running, new_status):
    test_to_find_status_running.edit_status(new_status)
    test_to_find_status_running.refresh()
    success_tests = client.query_tests().filter(status='RUNNING')
    assert len(success_tests) == 0
    [test] = client.query_tests().filter(status=new_status)
    assert test == test_to_find_status_running


def test_search_by_status_failure(client, test_to_find_status_failure):
    [test] = client.query_tests().filter(status='FAILURE')
    assert test == test_to_find_status_failure


@pytest.mark.parametrize('new_status', ['SUCCESS', 'SKIPPED', 'RUNNING', 'ERROR', 'INTERRUPTED'])
def test_search_by_status_failure_modified(client, test_to_find_status_failure, new_status):
    test_to_find_status_failure.edit_status(new_status)
    test_to_find_status_failure.refresh()
    success_tests = client.query_tests().filter(status='FAILURE')
    assert len(success_tests) == 0
    [test] = client.query_tests().filter(status=new_status)
    assert test == test_to_find_status_failure


def test_search_by_status_error(client, test_to_find_status_error):
    [test] = client.query_tests().filter(status='ERROR')
    assert test == test_to_find_status_error


@pytest.mark.parametrize('new_status', ['SUCCESS', 'SKIPPED', 'RUNNING', 'FAILURE', 'INTERRUPTED'])
def test_search_by_status_error_modified(client, test_to_find_status_error, new_status):
    test_to_find_status_error.edit_status(new_status)
    test_to_find_status_error.refresh()
    success_tests = client.query_tests().filter(status='ERROR')
    assert len(success_tests) == 0
    [test] = client.query_tests().filter(status=new_status)
    assert test == test_to_find_status_error


def test_search_by_status_skipped(client, test_to_find_status_skipped):
    [test] = client.query_tests().filter(status='SKIPPED')
    assert test == test_to_find_status_skipped


@pytest.mark.parametrize('new_status', ['SUCCESS', 'ERROR', 'RUNNING', 'FAILURE', 'INTERRUPTED'])
def test_search_by_status_skipped_modified(client, test_to_find_status_skipped, new_status):
    test_to_find_status_skipped.edit_status(new_status)
    test_to_find_status_skipped.refresh()
    success_tests = client.query_tests().filter(status='SKIPPED')
    assert len(success_tests) == 0
    [test] = client.query_tests().filter(status=new_status)
    assert test == test_to_find_status_skipped


def test_search_by_status_interrupted(client, test_to_find_status_interrupted):
    [test] = client.query_tests().filter(status='INTERRUPTED')
    assert test == test_to_find_status_interrupted


@pytest.mark.parametrize('new_status', ['SUCCESS', 'ERROR', 'RUNNING', 'FAILURE', 'SKIPPED'])
def test_search_by_status_interrupted_modified(client, test_to_find_status_interrupted, new_status):
    test_to_find_status_interrupted.edit_status(new_status)
    test_to_find_status_interrupted.refresh()
    success_tests = client.query_tests().filter(status='INTERRUPTED')
    assert len(success_tests) == 0
    [test] = client.query_tests().filter(status=new_status)
    assert test == test_to_find_status_interrupted


def test_edit_bad_status(client, test_to_find_status_success):
    with raises_bad_request():
        test_to_find_status_success.edit_status('BAD_STATUS')


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
    test.mark_skipped()
    test.report_end()
    test.refresh()
    return test


@pytest.fixture
def test_to_find_status_interrupted(started_session):
    test = started_session.report_test_start()
    test.mark_interrupted()
    test.report_end()
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



