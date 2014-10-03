import socket

import flux

import pytest

from .utils import raises_not_found, raises_conflict


def test_start_session(client):
    session = client.report_session_start()
    assert session


def test_start_session_logical_id(client):
    logical_id = '1'
    session = client.report_session_start(logical_id=logical_id)
    assert session


def test_start_session_no_logical_id(client):
    session = client.report_session_start()
    assert session


def test_started_session_hostname(started_session):
    assert started_session.hostname == socket.getfqdn()


def test_started_session_hostname_specify_explicitly(client):
    hostname = 'some_hostname'
    session = client.report_session_start(hostname=hostname)
    assert session.hostname == hostname


def test_start_session_with_product(client, product_info):
    session = client.report_session_start(
        **dict(('product_{0}'.format(k), v) for k, v in product_info.items()))
    assert session.product_name == product_info.get('name')
    assert session.product_version == product_info.get('version')
    assert session.product_revision == product_info.get('revision')


def test_session_set_product(started_session, product_info):
    assert started_session.product_name is None
    started_session.set_product(**product_info)
    started_session.refresh()
    assert started_session.product_name == product_info.get('name')
    assert started_session.product_version == product_info.get('version')
    assert started_session.product_revision == product_info.get('revision')


def test_session_set_user(started_session):
    assert started_session.user_name is None
    user_name = 'user1'
    started_session.set_user(user_name)
    started_session.refresh()
    assert started_session.user_name == user_name


def test_session_set_product_nonexistent_session(nonexistent_session, product_info):
    with raises_not_found():
        nonexistent_session.set_product(**product_info)


def test_session_add_user_nonexistent_session(nonexistent_session):
    with raises_not_found():
        user_name = 'user1'
        nonexistent_session.set_user(user_name)



def test_started_session_times(started_session):
    assert started_session.start_time is not None
    assert started_session.end_time is None


def test_query_all_sessions(client, started_session):
    [session] = client.query_sessions()
    assert session.id == started_session.id
    assert session == started_session


def test_query_all_tests(client, started_test):
    [test] = client.query_tests()
    assert test.id == started_test.id
    assert test == started_test


@pytest.mark.parametrize('use_duration', [True, False])
def test_end_session(started_session, use_duration):
    duration = 10
    start_time = started_session.start_time
    if use_duration:
        started_session.report_end(duration=duration)
    else:
        flux.current_timeline.sleep(10)
        started_session.report_end()
    started_session.refresh()
    assert started_session.end_time == start_time + duration


def test_end_session_doesnt_exist(nonexistent_session):
    with raises_not_found():
        nonexistent_session.report_end()


def test_end_session_twice(ended_session):
    with raises_conflict():
        ended_session.report_end()


def test_session_status_running(started_session):
    started_session.refresh()
    assert started_session.status == 'RUNNING'


def test_session_status_finished(ended_session):
    ended_session.refresh()
    assert ended_session.status == 'SUCCESS'


def test_session_status_failure(started_session_with_ended_test):
    (started_session, test) = started_session_with_ended_test
    test.add_failure()
    started_session.report_end()
    started_session.refresh()
    assert started_session.status == 'FAILURE'


def test_session_status_error(started_session_with_ended_test):
    (started_session, test) = started_session_with_ended_test
    test.add_error()
    started_session.report_end()
    started_session.refresh()
    assert started_session.status == 'FAILURE'


def test_session_status_error_and_failure(started_session_with_ended_test):
    (started_session, test) = started_session_with_ended_test
    test.add_error()
    test.add_failure()
    started_session.report_end()
    started_session.refresh()
    assert started_session.status == 'FAILURE'


def test_session_query_tests(started_session_with_ended_test):
    (started_session, test) = started_session_with_ended_test
    [queried_test] = started_session.query_tests()
    assert queried_test.id == test.id
    test.refresh()  # need to update end_time
    assert queried_test == test
