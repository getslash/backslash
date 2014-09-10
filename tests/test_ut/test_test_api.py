from uuid import uuid1

import requests

import pytest


def test_start_test(started_session, started_test, test_name):
    test = started_session.report_test_start(name=test_name)
    assert test is not None

def test_test_session_id(started_session, started_test):
    assert started_test.session_id == started_session.id

def test_cannot_start_test_ended_session(ended_session):
    with pytest.raises(requests.HTTPError) as caught:
        ended_session.report_test_start(name='name')
    assert caught.value.response.status_code == requests.codes.conflict

def test_cannot_start_test_nonexistent_session(nonexistent_session):
    with pytest.raises(requests.HTTPError) as caught:
        nonexistent_session.report_test_start(name='name')
    assert caught.value.response.status_code == requests.codes.not_found



@pytest.fixture
def test_name():
    return 'test_{0}'.format(uuid1())

@pytest.fixture
def started_test(started_session, test_name):
    return started_session.report_test_start(name=test_name)
