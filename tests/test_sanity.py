import requests

def test_sanity(backslash_url):
    requests.get(backslash_url).raise_for_status()
