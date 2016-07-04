import pytest


def test_debug(app_config):
    assert isinstance(app_config['debug'], bool)


@pytest.fixture
def app_config(client):
    return client.api.call_function('get_app_config')
