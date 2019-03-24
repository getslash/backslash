from uuid import uuid4

import flux
import pytest
from flask_app import models


def test_start_session(
    client, fake_email, proxy_role, request  # pylint: disable=unused-argument
):
    session = client.report_session_start(user_email=fake_email)
    assert models.User.query.filter_by(email=fake_email).count() == 1
    assert session


def test_start_session_proxy_generates_activity_for_user(
    client,
    fake_email,
    testuser_id,
    proxy_role,  # pylint: disable=unused-argument
    request,  # pylint: disable=unused-argument
):
    flux.current_timeline.sleep(1)
    client.report_session_start(user_email=fake_email)

    assert (
        models.User.query.filter_by(email=fake_email).one().last_activity
        == flux.current_timeline.time()
    )
    assert (
        models.User.query.get(testuser_id).last_activity == flux.current_timeline.time()
    )

    flux.current_timeline.sleep(1)


@pytest.fixture
def fake_email(request):
    returned = "{}@something.com".format(uuid4())
    assert models.User.query.filter_by(email=returned).count() == 0

    @request.addfinalizer
    def cleanup():  # pylint: disable=unused-variable
        models.User.query.filter_by(email=returned).delete()
        models.db.session.commit()

    return returned


@pytest.fixture(autouse=True)
def db_context_active(active_db_context):  # pylint: disable=unused-argument
    pass
