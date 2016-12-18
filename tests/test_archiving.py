from .utils import raises_forbidden, raises_not_found


def test_regular_user_cant_archive(client, ended_session, real_login):
    with raises_forbidden():
        ended_session.toggle_archived()

def test_archive_session(client, ended_session, real_login, moderator_role):
    ended_session.toggle_archived()
    for index, session in enumerate(client.query_sessions()):
        if index > 500:
            break
        assert session.id != ended_session.id

def test_archive_unarchive_session(client, ended_session, real_login, moderator_role):
    ended_session.toggle_archived()
    assert ended_session.refresh().archived
    ended_session.toggle_archived()
    assert not ended_session.refresh().archived


def test_archive_nonexistent_session(client, nonexistent_session, real_login, moderator_role):
    with raises_not_found():
        nonexistent_session.toggle_archived()
