import pytest
from uuid import uuid4


@pytest.mark.parametrize('use_logical_id', [False, True])
def test_get_errors_by_logical_id(container, error, client, use_logical_id):
    errors = _get_errors(client, **{f'{container.type}_id': container.logical_id if use_logical_id else container.id})
    assert len(errors) == 1
    assert errors[0]['id'] == error.id


def _get_errors(client, **kwargs):
    return client.api.get('/rest/errors', params=kwargs)['errors']

@pytest.fixture(params=['session', 'test'])
def container(request, client):
    typename = request.param
    session = client.report_session_start(logical_id=str(uuid4()))
    if typename == 'session':
        return session
    elif typename == 'test':
        return session.report_test_start(test_logical_id=str(uuid4()), name='bla')

    raise NotImplementedError() # pragma: no cover


@pytest.fixture
def error(container):
    returned = container.add_error('exception', 'ExceptionType')
    return returned
