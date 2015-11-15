import requests


def test_activity_by_user(client, testuser_id, real_login):
    assert _get_activities(client, {'user_id': testuser_id}) == []


def test_investigate_activity(client, ended_session, real_login):
    ended_session.toggle_investigated()
    [a1] = _get_activities(client, {'session_id': ended_session.id})
    assert a1.action == 'investigated'
    ended_session.toggle_investigated()
    [a1, a2] = _get_activities(client, {'session_id': ended_session.id})
    assert a1.action == 'investigated'
    assert a2.action == 'uninvestigated'
    assert a1.timestamp < a2.timestamp


def test_archive_activity(client, ended_session, real_login, moderator_role):
    ended_session.toggle_archived()
    [a1] = _get_activities(client, {'session_id': ended_session.id})
    assert a1.action == 'archived'
    ended_session.toggle_archived()
    [a1, a2] = _get_activities(client, {'session_id': ended_session.id})
    assert a1.action == 'archived'
    assert a2.action == 'unarchived'
    assert a1.timestamp < a2.timestamp


def _get_activities(client, params):
    return client.api.session.get(
        client.api.url.add_path('rest/activities'),
        params=params).json()['activities']
