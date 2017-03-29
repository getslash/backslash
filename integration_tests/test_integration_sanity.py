import requests

def test_integration_sanity(integration_url):
    assert requests.get(integration_url).ok
