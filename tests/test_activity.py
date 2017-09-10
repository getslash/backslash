import flux

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
