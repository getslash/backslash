from .utils import raises_not_found

def test_archive_session(client, ended_session):
    client.do_real_login()
    ended_session.toggle_archived()
    for session in client.query_sessions():
        assert session.id != ended_session.id

def test_archive_unarchive_session(client, ended_session):
    client.do_real_login()
    ended_session.toggle_archived()
    assert ended_session.refresh().archived
    ended_session.toggle_archived()
    assert not ended_session.refresh().archived


def test_archive_nonexistent_session(client, nonexistent_session):
    client.do_real_login()
    with raises_not_found():
        nonexistent_session.toggle_archived()

