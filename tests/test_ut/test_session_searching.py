import pytest


def test_search_by_product_name(client, sessions, session_to_find_product, product_info):
    [session] = client.query_sessions().filter(product_name=product_info['name'])
    assert session == session_to_find_product


def test_search_by_user(client, sessions, session_to_find_user, user_name):
    [session] = client.query_sessions().filter(user_name=user_name)
    assert session == session_to_find_user


def test_search_by_status_running(client, sessions, session_to_find_status_running):
    [session] = client.query_sessions().filter(status='RUNNING')
    assert session == session_to_find_status_running
#   empty result is not supported yet
#   [success_session] = client.query_sessions().filter(status='SUCCESS')
#    assert len(success_session) == 0


def test_search_by_status_success(client, sessions, session_to_find_status_success):
    [session] = client.query_sessions().filter(status='SUCCESS')
    assert session == session_to_find_status_success


def test_search_by_status_failure_failed_test(client, sessions, session_to_find_status_failed_test):
    [session] = client.query_sessions().filter(status='FAILURE')
    assert session == session_to_find_status_failed_test


def test_search_by_status_failure_error_test(client, sessions, session_to_find_status_error_test):
    [session] = client.query_sessions().filter(status='FAILURE')
    assert session == session_to_find_status_error_test


def test_search_by_session_logical_id(client, session_to_find_logical_id, logical_id):
    [session] = client.query_sessions().filter(logical_id=logical_id)
    assert session == session_to_find_logical_id


#just to see we can filter according to more than one field
def test_search_by_user_and_product(client, sessions, session_to_find_user_and_product, user_name, product_info):
    [session] = client.query_sessions().filter(product_name=product_info['name'], user_name=user_name)
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
    num_sessions = 3
    for i in range(num_sessions):
        s = client.report_session_start()
        s.report_end()
    assert len(client.query_sessions()) == num_sessions

