import pytest
from .utils import raises_forbidden


def test_start_session_by_delegate_forbidden_no_role(client, otheruser_email):
    with raises_forbidden():
        client.report_session_start(user_email=otheruser_email)


def test_start_session_delegate(client, testuser_email, otheruser_email, proxy_role):
    session = client.report_session_start(user_email=otheruser_email)
    session.report_end()
    assert session.user_email == otheruser_email
    assert session.real_email == testuser_email

def test_can_delegate_to_self(client, testuser_email):
    session = client.report_session_start(user_email=testuser_email)
    session.report_end()
    assert session.user_email == testuser_email
    assert session.real_email is None
