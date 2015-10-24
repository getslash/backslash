from uuid import uuid4

import pytest


def test_get_by_logical_id(client, logical_id_object, logical_id, logical_id_url, logical_id_object_type):
    returned = client.api.session.get(logical_id_url)
    returned.raise_for_status()
    assert returned.json()[logical_id_object_type]['id'] == logical_id_object.id


@pytest.fixture
def logical_id():
    return str(uuid4())

@pytest.fixture
def logical_id_object(client, logical_id_object_type, logical_id):
    session = client.report_session_start(logical_id=logical_id)
    if logical_id_object_type == 'session':
        return session
    elif logical_id_object_type == 'test':
        return session.report_test_start(name='name', test_logical_id=logical_id)

    raise NotImplementedError() # pragma: no cover

@pytest.fixture(params=['test', 'session'])
def logical_id_object_type(request):
    return request.param

@pytest.fixture
def logical_id_url(webapp, logical_id, logical_id_object_type):
    return webapp.url.add_path('rest/{}s/{}'.format(logical_id_object_type, logical_id))
