import pytest


def test_debug(app_config):
    assert isinstance(app_config['debug'], bool)

def test_oauth_client_id(app_config):
    assert 'google_oauth2_client_id' in app_config


@pytest.fixture
def app_config(client):
    cfg = client.api.call.get_app_config()
    if cfg['setup_needed']:
        client.api.call.setup(config={
            'admin_email': 'admin@localhost',
            'admin_password': '123456',
        })
    return client.api.call.get_app_config()
