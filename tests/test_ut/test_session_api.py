import socket

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


@pytest.fixture
def started_session(client):
    return client.report_session_start()
