# pylint: disable=unused-argument,protected-access
from uuid import uuid4

import requests

import pytest


def test_default_preferences(client, webapp, real_login):
    prefs = client.api.call.get_preferences()
    assert prefs == webapp.app.config['DEFAULT_PREFERENCES']


def test_set_preference(client, real_login, preference, orig_value, new_value):
    assert _get_pref(client, preference) == orig_value
    _set_pref(client, preference, new_value)
    assert _get_pref(client, preference) == new_value


def test_set_preference_multiple_times(client, real_login, preference, orig_value, new_value):
    assert _get_pref(client, preference) == orig_value
    num_tries = 10
    for i in range(1, num_tries + 1):
        _set_pref(client, preference, i)
    assert _get_pref(client, preference) == num_tries


def test_unset_preference(client, real_login, preference, orig_value, new_value):
    assert _get_pref(client, preference) == orig_value
    _set_pref(client, preference, new_value)
    _unset_pref(client, preference)
    assert _get_pref(client, preference) == orig_value

def test_set_unknown_preference(client, real_login):
    with pytest.raises(requests.HTTPError) as caught:
        _set_pref(client, 'unknown_pref', 'value')
    assert caught.value.response.status_code == requests.codes.bad_request


def _get_pref(client, preference):
    return client.api.call.get_preferences()[preference]


def _set_pref(client, preference, value):
    res = client.api.call.set_preference(preference=preference, value=value)
    assert res == value


def _unset_pref(client, preference):
    client.api.call.unset_preference(preference=preference)



@pytest.fixture
def preference():
    return 'time_format'


@pytest.fixture
def orig_value(webapp, preference):
    return webapp.app.config['DEFAULT_PREFERENCES'][preference]


@pytest.fixture
def new_value():
    return str(uuid4())
