from uuid import uuid4

from flask_app import models

import pytest


def test_start_session(client, fake_email, proxy_role, request): # pylint: disable=unused-argument
    assert models.User.query.filter_by(email=fake_email).count() == 0

    session = client.report_session_start(user_email=fake_email)

    @request.addfinalizer
    def cleanup():              # pylint: disable=unused-variable
        models.User.query.filter_by(email=fake_email).delete()
        models.db.session.commit()

    assert models.User.query.filter_by(email=fake_email).count() == 1
    assert session


@pytest.fixture
def fake_email():
    return '{}@something.com'.format(uuid4())


@pytest.fixture(autouse=True)
def db_context_active(active_db_context):  # pylint: disable=unused-argument
    pass
