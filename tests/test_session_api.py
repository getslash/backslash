# pylint: disable=unused-argument
import socket

import flux
import pytest

from .utils import raises_conflict, raises_not_found, without_single_rendered_fields


def test_start_session(client):
    session = client.report_session_start()
    assert session


def test_session_user_email(client, started_session, testuser_email):
    assert started_session.user_email == testuser_email


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


def test_session_user(started_session, testuser_id):
    assert started_session.user_id == testuser_id


def test_started_session_times(started_session):
    assert started_session.start_time is not None
    assert started_session.end_time is None



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


def test_session_status_failure_after_test_end(started_session_with_ended_test):
    (started_session, test) = started_session_with_ended_test
    test.add_failure('failure')
    test.refresh()
    assert test.status == 'FAILURE'
    started_session.report_end()
    started_session.refresh()
    assert started_session.status == 'FAILURE'


def test_session_status_error_after_test_end(started_session_with_ended_test):
    (started_session, test) = started_session_with_ended_test
    test.add_error('error')
    started_session.report_end()
    started_session.refresh()
    assert started_session.status == 'ERROR'


def test_session_status_error_and_failure(started_session_with_ended_test):
    (started_session, test) = started_session_with_ended_test
    test.add_error('error')
    test.add_failure('failure')
    started_session.report_end()
    started_session.refresh()
    assert started_session.status == 'ERROR'


def test_session_query_tests(started_session_with_ended_test):
    (started_session, test) = started_session_with_ended_test
    [queried_test] = started_session.query_tests()
    assert queried_test.id == test.id
    test.refresh()  # need to update end_time
    assert queried_test == without_single_rendered_fields(test)

