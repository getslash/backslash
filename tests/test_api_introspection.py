import pytest


def test_api_methods(api_info):
    assert api_info.endpoints.report_test_start.version >= 1


@pytest.fixture
def api_info(client):
    return client.api.info()
