import flux

import pytest
from backslash import FIELDS
from .utils import raises_bad_request


@pytest.fixture(autouse=True, scope='function')
def skip():
    pytest.skip()

def test_sessions_have_different_start_end_times(sessions):
    """Mostly checks that the fixture is sane, not an actual product test
    """
    times = set()
    for session in sessions:
        times.add(session.start_time)
        times.add(session.end_time)
    assert len(times) == len(sessions) * 2


def test_search_by_start_time_range(client, session_triplet):
    a, b, c = session_triplet
    assert a.start_time < b.start_time < c.start_time
    [matching] = client.query_sessions().filter(a.start_time+1 < FIELDS.start_time < c.start_time-1)
    assert matching == b


def test_search_by_product_name(client, sessions, session_to_find_product, product_info):
    [session] = client.query_sessions().filter(
        product_name=product_info['name'])
    assert session == session_to_find_product


def test_search_by_user(client, sessions, session_to_find_user, user_name):
    [session] = client.query_sessions().filter(user_name=user_name)
    assert session == session_to_find_user


def test_search_by_bad_filter_name(client):
    with raises_bad_request():
        # because of lazy evaluation we need to assign and "use" the result
        [dontcare] = client.query_sessions().filter(
            nonexistant_name='dontcare')


@pytest.mark.parametrize('new_status', ['SUCCESS', 'FAILURE'])
def test_search_by_status_running_modified(client, sessions, session_to_find_status_running, new_status):
    session_to_find_status_running.edit_status(new_status)
    session_to_find_status_running.refresh()

    running_query = client.query_sessions().filter(status='RUNNING')
    assert len(running_query) == 0
    [session] = client.query_sessions().filter(status=new_status)
    assert session == session_to_find_status_running


@pytest.mark.parametrize('new_status', ['RUNNING', 'FAILURE'])
def test_search_by_status_success_modified(client, sessions, session_to_find_status_success, new_status):
    session_to_find_status_success.edit_status(new_status)
    session_to_find_status_success.refresh()

    running_query = client.query_sessions().filter(status='SUCCESS')
    assert len(running_query) == 0
    [session] = client.query_sessions().filter(status=new_status)
    assert session == session_to_find_status_success


@pytest.mark.parametrize('new_status', ['RUNNING', 'SUCCESS'])
def test_search_by_status_failure_modified(client, sessions, session_to_find_status_failed_test, new_status):
    session_to_find_status_failed_test.edit_status(new_status)
    session_to_find_status_failed_test.refresh()

    running_query = client.query_sessions().filter(status='FAILURE')
    assert len(running_query) == 0
    [session] = client.query_sessions().filter(status=new_status)
    assert session == session_to_find_status_failed_test


def test_edit_bad_status(client, sessions, session_to_find_status_success):
    with raises_bad_request():
        session_to_find_status_success.edit_status('BAD_STATUS')


def test_search_by_status_running(client, sessions, session_to_find_status_running):
    [session] = client.query_sessions().filter(status='RUNNING')
    assert session == session_to_find_status_running
    success_query = client.query_sessions().filter(status='SUCCESS')
    assert len(success_query) == 0


def test_search_by_status_success(client, sessions, session_to_find_status_success):
    [session] = client.query_sessions().filter(status='SUCCESS')
    assert session == session_to_find_status_success


def test_search_by_bad_status(client):
    with raises_bad_request():
        # because of lazy evaluation we need to assign and "use" the result
        [dontcare] = client.query_sessions().filter(status='BADSTATUS')


def test_search_by_status_failure_failed_test(client, sessions, session_to_find_status_failed_test):
    [session] = client.query_sessions().filter(status='FAILURE')
    assert session == session_to_find_status_failed_test


def test_search_by_status_failure_error_test(client, sessions, session_to_find_status_error_test):
    [session] = client.query_sessions().filter(status='FAILURE')
    assert session == session_to_find_status_error_test


def test_search_by_session_logical_id(client, session_to_find_logical_id, logical_id):
    [session] = client.query_sessions().filter(logical_id=logical_id)
    assert session == session_to_find_logical_id


# just to see we can filter according to more than one field
def test_search_by_user_and_product(client, sessions, session_to_find_user_and_product, user_name, product_info):
    [session] = client.query_sessions().filter(
        product_name=product_info['name'], user_name=user_name)
    assert session == session_to_find_user_and_product


@pytest.fixture
def user_name():
    return 'user1'


@pytest.fixture
def session_to_find_product(client, product_info, ):
    session = client.report_session_start()
    session.set_product(**product_info)
    session.report_end()
    session.refresh()
    return session


@pytest.fixture
def session_to_find_user(client, user_name):
    session = client.report_session_start()
    session.set_user(user_name)
    session.report_end()
    session.refresh()
    return session


@pytest.fixture
def session_to_find_status_running(client):
    session = client.report_session_start()
    session.refresh()
    return session


@pytest.fixture
def session_to_find_status_success(client):
    session = client.report_session_start()
    session.report_end()
    session.refresh()
    return session


@pytest.fixture
def session_to_find_status_success(client):
    session = client.report_session_start()
    test = session.report_test_start()
    test.report_end()
    session.report_end()
    session.refresh()
    return session


@pytest.fixture
def session_to_find_status_failed_test(client):
    session = client.report_session_start()
    test = session.report_test_start()
    test.add_failure()
    test.report_end()
    session.report_end()
    session.refresh()
    return session


@pytest.fixture
def session_to_find_status_error_test(client):
    session = client.report_session_start()
    test = session.report_test_start()
    test.add_error()
    test.report_end()
    session.report_end()
    session.refresh()
    return session


@pytest.fixture
def session_to_find_user_and_product(client, user_name, product_info, ):
    session = client.report_session_start()
    session.set_user(user_name)
    session.set_product(**product_info)
    session.report_end()
    session.refresh()
    return session


@pytest.fixture
def session_to_find_logical_id(client, logical_id):
    session = client.report_session_start(logical_id=logical_id)
    session.report_end()
    session.refresh()
    return session


@pytest.fixture
def sessions(client):
    returned = []
    num_sessions = 5
    for i in range(num_sessions):
        flux.current_timeline.sleep(10)
        s = client.report_session_start()
        flux.current_timeline.sleep(10)
        s.report_end()
        s.refresh()
        returned.append(s)
    assert len(client.query_sessions()) == num_sessions
    return returned


@pytest.fixture
def session_triplet(sessions):
    return sessions[2], sessions[3], sessions[4]
