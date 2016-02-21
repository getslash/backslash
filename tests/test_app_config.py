def test_app_config(client):
    cfg = client.api.call_function('get_app_config')
    assert isinstance(cfg['debug'], bool)
