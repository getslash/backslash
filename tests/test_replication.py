import pytest
from .utils import raises_forbidden

def test_cannot_create_replication_no_admin_role(client, real_login):
    with raises_forbidden():
        client.api.call.create_replication(url='bla', index_name='bla')


def test_create_replication_admin(client, replication):
    pass


def test_replication_list(client, replication):
    replicas = client.api.get('rest/replications')['replications']
    assert replication['id'] in [r['id'] for r in replicas]
    for replica in replicas:
        assert 'username' in replica
        assert 'password' not in replica

def test_replication_delete(client, admin_role, real_login):
    replication1 = client.api.call.create_replication(url='1', index_name='bla')
    replication2 = client.api.call.create_replication(url='2', index_name='bla')
    prev_len = len(client.api.get('rest/replications')['replications'])
    assert prev_len >= 2
    client.api.call.delete_replication(id=replication2['id'])
    assert len(client.api.get('rest/replications')['replications']) == prev_len - 1


@pytest.fixture
def replication(client, real_login, admin_role, request):
    replication = client.api.call.create_replication(url='bla', username='bloop', index_name='bla')

    @request.addfinalizer
    def cleanup():
        client.api.call.delete_replication(id=replication['id'])
    return replication
