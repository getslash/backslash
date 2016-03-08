# pylint: disable=unused-argument

def test_user_capabilities(client, real_login, testuser_id):
    caps = client.api.get('/rest/users/{}'.format(testuser_id))['user']['capabilities']
    assert caps['comment_test'] is True
