from flask_app import models
from .utils import raises_forbidden


def test_toggle_role(client, otheruser_id, admin_role, db_context, real_login):
    with db_context():
        assert models.User.query.get(otheruser_id).roles == []

    client.toggle_user_role(user_id=otheruser_id, role='proxy')

    with db_context():
        assert models.User.query.get(otheruser_id).roles == ['proxy']

    client.toggle_user_role(user_id=otheruser_id, role='proxy')

    with db_context():
        assert models.User.query.get(otheruser_id).roles == []


def test_cannot_toggle_when_non_admin(client, otheruser_id, db_context, role, real_login):

    with raises_forbidden():
        client.toggle_user_role(user_id=otheruser_id, role=role)


def test_get_user_tokens(client, otheruser_id, admin_role, real_login):
    assert client.get_user_run_tokens(user_id=otheruser_id) == []


def test_get_user_tokens_forbidden_non_admin(client, otheruser_id, real_login):
    with raises_forbidden():
        client.get_user_run_tokens(user_id=otheruser_id)


def test_get_user_tokens_allowed_own_user(client, testuser_id, real_login, runtoken):
    assert client.get_user_run_tokens(user_id=testuser_id) == [runtoken]
