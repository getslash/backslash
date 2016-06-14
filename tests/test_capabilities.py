# pylint: disable=unused-argument

def test_user_capabilities(client, real_login):
    caps = client.api.get('/rest/users/self').capabilities
    assert caps['comment_test'] is True
