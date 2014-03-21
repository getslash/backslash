import requests

def test_index_view(webapp):
    webapp.get("/").raise_for_status()

def test_not_found_errors(webapp):
    assert webapp.get("/nonexistent_path").status_code == requests.codes.not_found


