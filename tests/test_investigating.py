from .utils import raises_not_found

from flask_app import activity

def test_toggle_investigated(client, ended_session, real_login):
    assert not ended_session.investigated
    ended_session.toggle_investigated()
    assert ended_session.refresh().investigated
    ended_session.toggle_investigated()
    assert not ended_session.refresh().investigated


