import requests


def test_sanity(webapp_url):
    requests.get(webapp_url).raise_for_status()
