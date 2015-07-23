from .utils import raises_not_found

def test_archive_session(client, ended_session):
    ended_session.archive()
    for session in client.query_sessions():
        assert session.id != ended_session.id

def test_archive_nonexistent_session(client, nonexistent_session):
    with raises_not_found():
        nonexistent_session.archive()

