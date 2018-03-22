import flux
import pytest

from flask_app import models


def test_user_last_activity(client, testuser_id, db_context):
    s = client.report_session_start()
    start_time = flux.current_timeline.time() # pylint: disable=no-member

    def get_last_active():
        with db_context():
            return models.User.query.get(testuser_id).last_activity

    l1 = get_last_active()
    assert l1 == start_time

    flux.current_timeline.sleep(1) # pylint: disable=no-member

    _ = s.get_metadata()
    l2 = get_last_active()
    assert l2 == l1


@pytest.mark.parametrize('with_keepalive', [True, False])
def test_subject_last_activity(client, subjects, db_context, with_keepalive):
    session = client.report_session_start(
        subjects=subjects,
        **({'keepalive_interval': 60} if with_keepalive else {}))

    def get_last_active():
        with db_context():
            return models.Subject.query.filter_by(name=subjects[0]['name']).one().last_activity

    assert get_last_active() == flux.current_timeline.time()
    flux.current_timeline.sleep(1)
    session.send_keepalive()
    assert get_last_active() == flux.current_timeline.time()
    flux.current_timeline.sleep(1)
    session.report_end()
    assert get_last_active() == flux.current_timeline.time()
