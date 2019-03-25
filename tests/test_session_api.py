# pylint: disable=unused-argument
import socket

import flux
import pytest

from .utils import (
    raises_conflict,
    raises_not_found,
    without_single_rendered_fields,
    raises_bad_request,
)


def test_start_session(client):
    session = client.report_session_start()
    assert session


def test_session_user_email(client, started_session, testuser_email):
    assert started_session.user_email == testuser_email


def test_start_session_logical_id(client):
    logical_id = "1"
    session = client.report_session_start(logical_id=logical_id)
    assert session


def test_start_session_no_logical_id(client):
    session = client.report_session_start()
    assert session


def test_started_session_hostname(started_session):
    assert started_session.hostname == socket.getfqdn()


def test_started_session_hostname_specify_explicitly(client):
    hostname = "some_hostname"
    session = client.report_session_start(hostname=hostname)
    assert session.hostname == hostname


def test_session_user(started_session, testuser_id):
    assert started_session.user_id == testuser_id


def test_started_session_times(started_session):
    assert started_session.start_time is not None
    assert started_session.end_time is None


@pytest.mark.parametrize("use_duration", [True, False])
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
    assert started_session.status == "RUNNING"


def test_session_status_finished(ended_session):
    ended_session.refresh()
    assert ended_session.status == "SUCCESS"


def test_session_status_failure_after_test_end(started_session_with_ended_test):
    (started_session, test) = started_session_with_ended_test
    test.add_failure("failure")
    test.refresh()
    assert test.status == "FAILURE"
    started_session.report_end()
    started_session.refresh()
    assert started_session.status == "FAILURE"


def test_session_status_error_after_test_end(started_session_with_ended_test):
    (started_session, test) = started_session_with_ended_test
    test.add_error("error")
    started_session.report_end()
    started_session.refresh()
    assert started_session.status == "ERROR"


def test_session_status_error_and_failure(started_session_with_ended_test):
    (started_session, test) = started_session_with_ended_test
    test.add_error("error")
    test.add_failure("failure")
    started_session.report_end()
    started_session.refresh()
    assert started_session.status == "ERROR"


def test_session_query_tests(started_session_with_ended_test):
    (started_session, test) = started_session_with_ended_test
    [queried_test] = started_session.query_tests()
    assert queried_test.id == test.id
    test.refresh()  # need to update end_time
    assert queried_test == without_single_rendered_fields(test)


@pytest.mark.parametrize("report_end", [True, False])
def test_report_interrupted(started_session, report_end):
    started_session.report_interrupted()
    if report_end:
        started_session.report_end()
    assert started_session.refresh().status.lower() == "interrupted"


def test_report_interrupted_ended_session(started_session):
    started_session.report_end()
    started_session.report_interrupted()
    assert started_session.refresh().status.lower() == "interrupted"


@pytest.mark.parametrize("has_fatal_errors", [True, False])
def test_session_end_with_fatal_errors(started_session, has_fatal_errors):
    started_session.report_end(has_fatal_errors=has_fatal_errors)
    assert started_session.refresh().has_fatal_errors == has_fatal_errors


def test_session_ttl_cant_provide_without_keepalive(client):
    with raises_bad_request():
        client.report_session_start(ttl_seconds=100)


def test_session_ttl_null_by_default(started_session):
    assert started_session.ttl_seconds is None
    assert started_session.delete_at is None


def test_session_ttl_on_creation(ttl_session, ttl_seconds, keepalive_interval):
    assert ttl_session.ttl_seconds == ttl_seconds
    assert (
        ttl_session.delete_at
        == flux.current_timeline.time() + ttl_seconds + keepalive_interval
    )


def test_session_ttl_on_keepalive(client, ttl_session, ttl_seconds, keepalive_interval):
    sleep_seconds = 5
    flux.current_timeline.sleep(sleep_seconds)
    client.api.call.send_keepalive(session_id=ttl_session.id)
    ttl_session.refresh()
    assert ttl_session.ttl_seconds == ttl_seconds
    assert (
        ttl_session.delete_at
        == flux.current_timeline.time() + keepalive_interval + ttl_seconds
    )
    assert ttl_session.delete_at == ttl_session.next_keepalive + ttl_seconds


def test_session_ttl_on_session_end(client, ttl_session, ttl_seconds):
    sleep_seconds = 5
    flux.current_timeline.sleep(sleep_seconds)
    ttl_session.report_end()
    ttl_session.refresh()
    assert ttl_session.ttl_seconds == ttl_seconds
    assert ttl_session.delete_at == flux.current_timeline.time() + ttl_seconds


@pytest.mark.parametrize("child_has_delete_at", [True, False])
def test_parallel_session_discard(
    client, started_parallel_session, real_login, admin_role, child_has_delete_at
):
    parent, child = started_parallel_session
    if child_has_delete_at:
        client.api.call.discard_session(session_id=child.id, grace_period_seconds=100)
    assert parent.delete_at is None
    client.api.call.discard_session(session_id=parent.id, grace_period_seconds=1000)
    assert parent.refresh().delete_at is not None
    assert parent.delete_at == child.refresh().delete_at


@pytest.mark.parametrize("child_has_delete_at", [True, False])
@pytest.mark.parametrize("parent_has_delete_at", [True, False])
def test_parallel_session_preserve(
    client,
    started_parallel_session,
    real_login,
    admin_role,
    child_has_delete_at,
    parent_has_delete_at,
):

    parent, child = started_parallel_session
    if child_has_delete_at:
        client.api.call.discard_session(session_id=child.id, grace_period_seconds=100)
    if parent_has_delete_at:
        client.api.call.discard_session(session_id=parent.id, grace_period_seconds=100)
    assert parent.delete_at is None
    client.api.call.preserve_session(session_id=parent.id)
    assert parent.refresh().delete_at is None
    assert child.refresh().delete_at is None


def test_report_reporting_stopped(client, started_session):
    assert not started_session.reporting_stopped
    client.api.call.report_reporting_stopped(session_id=started_session.id)
    started_session.refresh()
    assert started_session.end_time is None
    assert started_session.reporting_stopped
