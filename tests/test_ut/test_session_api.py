import socket

import flux
import requests

import pytest


def test_start_session(client):
    session = client.report_session_start()
    assert session


def test_started_session_hostname(started_session):
    assert started_session.hostname == socket.getfqdn()


def test_started_session_hostname_specify_explicitly(client):
    hostname = 'some_hostname'
    session = client.report_session_start(hostname=hostname)
    assert session.hostname == hostname


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
    with pytest.raises(requests.HTTPError) as caught:
        nonexistent_session.report_end()
    assert caught.value.response.status_code == requests.codes.not_found


def test_end_session_twice(ended_session):
    with pytest.raises(requests.HTTPError) as caught:
        ended_session.report_end()
    assert caught.value.response.status_code == requests.codes.conflict

