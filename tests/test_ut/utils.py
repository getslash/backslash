from contextlib import contextmanager

import requests

import pytest


def raises_conflict():
    return raises_http_error(requests.codes.conflict)

@contextmanager
def raises_http_error(status_code):
    with pytest.raises(requests.HTTPError) as caught:
        yield
    assert caught.value.response.status_code == status_code
