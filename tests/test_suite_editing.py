import requests

import pytest


def test_suite_name(suite_name, suite):
    assert suite.name == suite_name


def test_suite_invalid_name(invalid_suite_name, client, real_login):  # pylint: disable=unused-argument
    with pytest.raises(requests.HTTPError) as caught:
        client.api.call.create_suite(name=invalid_suite_name)
    assert caught.value.response.status_code == requests.codes.bad_request


def test_private_suites_duplicate_name(client, suite, suite_name):  # pylint: disable=unused-argument
    with pytest.raises(requests.HTTPError) as caught:
        client.api.call.create_suite(name=suite_name)
    assert caught.value.response.status_code == requests.codes.conflict
    assert 'naming conflict' in caught.value.response.json()['message']


def test_suite_unpublished_by_default(suite):
    assert suite.is_public is False


def test_suite_query(client, suite, testuser_id):
    suites = client.query(
        '/rest/suites', query_params={'owner': testuser_id}).all()
    assert suite in suites


def test_get_suite_items_empty(client, suite):
    assert client.api.call.get_suite_items(suite_id=suite.id)['items'] == []

##########################################################################


@pytest.fixture
def suite_name():
    suite_name = 'some_suite_name'
    return suite_name


@pytest.fixture(params=[''])
def invalid_suite_name(request):
    return request.param


@pytest.fixture
def suite(client, suite_name, real_login):  # pylint: disable=unused-argument
    suite = client.api.call.create_suite(name=suite_name)
    return suite
