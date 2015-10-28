# pylint: disable=unused-argument
import flux
import pytest


def test_no_keepalive_session(client):
    session = client.report_session_start()
    flux.current_timeline.sleep(3600)
    assert session.refresh().status == 'RUNNING'
    assert not session.refresh().is_abandoned


def test_keepalive_expiration(client, interval):
    session = client.report_session_start(keepalive_interval=interval)
    flux.current_timeline.sleep(interval / 2)
    assert session.refresh().status == 'RUNNING'
    assert not session.is_abandoned
    flux.current_timeline.sleep(interval / 2 + 1)
    assert session.refresh().status == 'RUNNING'
    assert session.is_abandoned


def test_keepalive(client, interval):
    session = client.report_session_start(keepalive_interval=interval)
    for _ in range(10):
        flux.current_timeline.sleep(interval)
        session.send_keepalive()
    assert not session.is_abandoned
    assert session.refresh().status == 'RUNNING'


def test_keepalive_not_counted_after_finish(client, interval):
    session = client.report_session_start(keepalive_interval=interval)
    session.report_end()
    flux.current_timeline.sleep(interval * 2)
    assert session.refresh().status == 'SUCCESS'
    assert not session.is_abandoned


@pytest.fixture
def interval():
    return 301
