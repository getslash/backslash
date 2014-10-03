from contextlib import contextmanager

import requests

import pytest


def raises_conflict():
    return raises_http_error(requests.codes.conflict)


def raises_bad_request():
    return raises_http_error(requests.codes.bad_request)


def raises_not_found():
    return raises_http_error(requests.codes.not_found)

@contextmanager
def raises_http_error(status_code):
    with pytest.raises(requests.HTTPError) as caught:
        yield
    assert caught.value.response.status_code == status_code
