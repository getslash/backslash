import requests

def test_sanity(deployment_webapp_url):
    requests.get(deployment_webapp_url).raise_for_status()
