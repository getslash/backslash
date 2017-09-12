# pylint: disable=unused-argument

def test_user_capabilities(client, real_login):
    [user] = client.query('/rest/users', query_params={'current_user': 'true'})
    caps = user.capabilities
    assert caps['comment_test'] is True
