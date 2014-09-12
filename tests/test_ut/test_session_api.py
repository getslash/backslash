import socket

import flux
import requests

import pytest


def test_start_session(client):
    logical_id = 1
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
    logical_id = 1
    session = client.report_session_start(logical_id=logical_id, hostname=hostname)
    assert session.hostname == hostname

def test_start_session_with_product_name(client):
    logical_id = 1
    product_name = 'foo'
    session = client.report_session_start(logical_id=logical_id, product_name=product_name)
    assert session.product_name == product_name
    assert session.product_version == None
    assert session.product_revision == None

def test_start_session_with_product_name_and_version(client):
    logical_id = 1
    product_name = 'foo'
    product_version = 'bar'
    session = client.report_session_start(logical_id=logical_id, product_name=product_name, product_version=product_version)
    assert session.product_name == product_name
    assert session.product_version == product_version
    assert session.product_revision == None

def test_start_session_with_full_product_name(client):
    logical_id = 1
    product_name = 'foo'
    product_version = 'bar'
    product_revision = 'qux'
    session = client.report_session_start(logical_id=logical_id, product_name=product_name,
                                          product_version=product_version, product_revision=product_revision)
    assert session.product_name == product_name
    assert session.product_version == product_version
    assert session.product_revision == product_revision

def test_start_session_with_full_product_name(started_session):
    product_name = 'foo'
    product_version = 'bar'
    product_revision = 'qux'
    started_session.set_product(name=product_name, version=product_version, revision=product_revision)
    started_session.refresh()
    assert started_session.product_name == product_name
    assert started_session.product_version == product_version
    assert started_session.product_revision == product_revision

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

