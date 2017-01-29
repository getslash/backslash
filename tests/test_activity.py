import pytest

import requests
import flux

from flask_app import models


def test_activity_by_user(client, testuser_id, real_login):
    assert _get_activities(client, {'user_id': testuser_id}) == []


def test_investigate_activity(client, ended_session, real_login):
    ended_session.toggle_investigated()
    [a1] = _get_activities(client, {'session_id': ended_session.id})
    assert a1['action'] == 'investigated'
    flux.current_timeline.sleep(1)
    ended_session.toggle_investigated()
    [a1, a2] = _get_activities(client, {'session_id': ended_session.id})
    assert a1['action'] == 'investigated'
    assert a2['action'] == 'uninvestigated'
    assert a1['timestamp'] < a2['timestamp']


def test_archive_activity(client, ended_session, real_login, moderator_role):
    ended_session.toggle_archived()
    [a1] = _get_activities(client, {'session_id': ended_session.id})
    assert a1['action'] == 'archived'
    flux.current_timeline.sleep(1)
    ended_session.toggle_archived()
    [a1, a2] = _get_activities(client, {'session_id': ended_session.id})
    assert a1['action'] == 'archived'
    assert a2['action'] == 'unarchived'
    assert a1['timestamp'] < a2['timestamp']


def test_comment_activity(client, commentable, real_login):
    comment = 'comment here'
    commentable.post_comment(comment)
    [a1] = _get_activities(client, commentable)
    assert a1['action'] == 'commented'
    assert a1['text'] == comment
    assert commentable.refresh().num_comments == 1


def test_user_last_activity(client, testuser_id, db_context):
    s = client.report_session_start()
    start_time = flux.current_timeline.time()

    def get_last_active():
        with db_context():
            return models.User.query.get(testuser_id).last_activity

    l1 = get_last_active()
    assert l1 == start_time

    flux.current_timeline.sleep(1)

    _ = s.get_metadata()
    l2 = get_last_active()
    assert l2 == l1


def test_delete_comment(commentable, real_login, client):
    pytest.skip('')


def _get_activities(client, params):
    if not isinstance(params, dict):
        params = {'{}_id'.format(params.type): params.id}

    return client.api.session.get(
        client.api.url.add_path('rest/activities'),
        params=params).json()['activities']
