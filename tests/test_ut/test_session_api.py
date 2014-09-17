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
    with pytest.raises(requests.HTTPError) as caught:
        session = client.report_session_start(logical_id=None)
    assert caught.value.response.status_code == requests.codes.bad_request

def test_started_session_hostname(started_session):
    assert started_session.hostname == socket.getfqdn()


def test_started_session_hostname_specify_explicitly(client):
    hostname = 'some_hostname'
    session = client.report_session_start(hostname=hostname)
    assert session.hostname == hostname

def test_start_session_with_product_name(client):
    product_name = 'foo'
    session = client.report_session_start(product_name=product_name)
    assert session.product_name == product_name
    assert session.product_version == None
    assert session.product_revision == None

def test_start_session_with_product_name_and_version(client):
    product_name = 'foo'
    product_version = 'bar'
    session = client.report_session_start(product_name=product_name, product_version=product_version)
    assert session.product_name == product_name
    assert session.product_version == product_version
    assert session.product_revision == None

def test_start_session_with_full_product_name(started_session, product_info):
    product_name = 'foo'
    product_version = 'bar'
    product_revision = 'qux'
    started_session.set_product(name=product_info['product_name'],
                                version=product_info['product_version'],
                                revision=product_info['product_revision'])
    started_session.refresh()
    assert started_session.product_name == product_name
    assert started_session.product_version == product_version
    assert started_session.product_revision == product_revision

def test_started_session_times(started_session):
    assert started_session.start_time is not None
    assert started_session.end_time is None


def test_query_all_sessions(client, started_session):
    [session] = client.query_sessions()
    assert session.id == started_session.id
    assert session == started_session


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

