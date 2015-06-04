import pytest
import requests

from backslash import Backslash


def test_requires_run_token(unauthorized_client, unauth_api):
    with pytest.raises(requests.HTTPError) as caught:
        unauth_api()
    assert caught.value.response.status_code == requests.codes.unauthorized


@pytest.fixture
def unauthorized_client(client, has_token):
    returned = Backslash(client._url, runtoken='invalid token')
    if not has_token:
        del returned.api.session.headers['X-Backslash-run-token']
    return returned


@pytest.fixture(params=[True, False])
def has_token(request):
    return request.param


def _start_new_session(client, unauthorized_client):
    return unauthorized_client.report_session_start

def _finish_running_session(client, unauthorized_client):
    session = client.report_session_start()
    session.client = unauthorized_client
    return session.report_end


@pytest.fixture(params=[
    _start_new_session,
    _finish_running_session,
])
def unauth_api(request, client, unauthorized_client):
    return request.param(client, unauthorized_client)
