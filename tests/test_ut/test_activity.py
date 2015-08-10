import pytest
from flask_app import activity
from flask_app.models import Activity


def test_no_user_activity_by_default(testuser_id, webapp):
    with webapp.app.app_context():
        assert Activity.query.filter(Activity.user_id==testuser_id).all() == []

def test_user_activity_archiving(testuser_id, ended_session, client, get_activities):
    client.do_real_login()
    ended_session.toggle_archived()
    [a] = get_activities()
    assert a.action == activity.ACTION_ARCHIVED
    ended_session.toggle_archived()
    _, a = get_activities()
    assert a.action == activity.ACTION_UNARCHIVED


@pytest.fixture
def get_activities(webapp, testuser_id):
    def returned():
        with webapp.app.app_context():
            return Activity.query.filter(Activity.user_id==testuser_id).all()
    return returned
