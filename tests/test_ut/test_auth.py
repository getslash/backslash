from flask_app.app import app

from flask.ext.security.utils import encrypt_password, verify_password

def test_verify_password_independent_of_salt():
    password = 'hello there'
    with app.app_context():
        encrypted = encrypt_password(password)
    assert encrypted != password
    app.config['SECURITY_PASSWORD_SALT'] = 'some other salt here'
    with app.app_context():
        assert verify_password(password, encrypted)
