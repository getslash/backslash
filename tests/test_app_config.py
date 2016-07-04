import pytest


def test_debug(app_config):
    assert isinstance(app_config['debug'], bool)

def test_oauth_client_id(app_config):
    assert 'oauth2_client_id' in app_config


@pytest.fixture
def app_config(client):
    return client.api.call_function('get_app_config')
