import pytest
import requests

from flask.ext.security.utils import encrypt_password, verify_password

def test_verify_password_independent_of_salt(webapp):
    app = webapp.app
    password = 'hello there'
    with app.app_context():
        encrypted = encrypt_password(password)
    assert encrypted != password
    app.config['SECURITY_PASSWORD_SALT'] = 'some other salt here'
    with app.app_context():
        assert verify_password(password, encrypted)

@pytest.mark.parametrize('path', ['/login', '/reauth'])
def test_unauthorized_post_to_login(webapp_without_login, path):
    resp = webapp_without_login.post(path, data={}, raw_response=True)

    assert resp.status_code == requests.codes.unauthorized
