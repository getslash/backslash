from .utils import raises_not_found

from flask_app import activity

def test_toggle_investigated(client, ended_session, real_login):
    assert not ended_session.investigated
    ended_session.toggle_investigated()
    assert ended_session.refresh().investigated
    ended_session.toggle_investigated()
    assert not ended_session.refresh().investigated


def test_investigate_activity(client, ended_session, real_login, get_activities):
    assert get_activities() == []
    ended_session.toggle_investigated()
    ended_session.toggle_investigated()
    [act1, act2] = get_activities()
    assert act1.action == activity.ACTION_INVESTIGATED
    assert act2.action == activity.ACTION_UNINVESTIGATED
