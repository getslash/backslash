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
