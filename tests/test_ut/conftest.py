from uuid import uuid1

import flux

import pytest


@pytest.fixture(autouse=True, scope='session')
def freeze_timeline(request):

    original_factor = flux.current_timeline.get_time_factor()

    @request.addfinalizer
    def finalizer():
        flux.current_timeline.set_time_factor(original_factor)

    flux.current_timeline.set_time_factor(0)


@pytest.fixture
def started_session(client):
    return client.report_session_start()


@pytest.fixture
def ended_session(client):
    # we don't use started_session to enable tests to use both...
    session = client.report_session_start()
    session.report_end()
    return session


@pytest.fixture
def nonexistent_session(client):
    from backslash.session import Session
    return Session(client, {'id': 238723287})


@pytest.fixture
def test_name():
    return 'test_{0}'.format(uuid1())


@pytest.fixture
def started_test(started_session, test_name):
    return started_session.report_test_start(name=test_name)


@pytest.fixture
def ended_test(started_session, test_name):
    returned = started_session.report_test_start(name=test_name)
    returned.report_end()
    return returned


@pytest.fixture
def nonexistent_test(client, started_session):
    from backslash.test import Test
    return Test(client, {'id': 6666, 'session_id': started_session.id})
