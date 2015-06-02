import os
import sys
import uuid

import requests
from flask.ext.loopback import FlaskLoopback
from urlobject import URLObject as URL

import pytest
from flask_app import app, models

from backslash import Backslash as BackslashClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def pytest_addoption(parser):
    parser.addoption("--url", action="store", default="http://127.0.0.1:8000")


@pytest.fixture
def client(webapp, runtoken):
    return BackslashClient('http://{0}'.format(webapp.hostname), runtoken=runtoken)

@pytest.fixture
def backslash_url(request):
    return URL(request.config.getoption("--url"))

@pytest.fixture(autouse=True)
def app_security_settings(webapp):
    webapp.app.config["SECRET_KEY"] = "testing_key"
    webapp.app.config["SECURITY_PASSWORD_SALT"] = webapp.app.extensions['security'].password_salt = "testing_salt"


@pytest.fixture
def webapp(request):
    returned = Webapp(app.create_app({
        'SQLALCHEMY_DATABASE_URI': 'postgresql://localhost/backslash-ut',
        'SECRET_KEY': 'testing-key',
        'TESTING': True,
    }))
    returned.activate()
    request.addfinalizer(returned.deactivate)
    return returned

@pytest.fixture(scope='function', autouse=True)
def db(request, webapp):
    with webapp.app.app_context():
        models.db.session.close()
        models.db.drop_all()
        models.db.create_all()
    return models.db

@pytest.fixture
def runtoken(db, webapp):
    with webapp.app.app_context():
        user = models.User(email='testing@localhost')
        db.session.add(user)
        token_string = 'some-token'
        token = models.RunToken(user_id=user.id, token=token_string)
        db.session.add(token)
        db.session.commit()
    return token_string

class Webapp(object):

    def __init__(self, app):
        super(Webapp, self).__init__()
        self.app = app
        self.loopback = FlaskLoopback(self.app)
        self.hostname = str(uuid.uuid1())

    def activate(self):
        self.loopback.activate_address((self.hostname, 80))

    def deactivate(self):
        self.loopback.deactivate_address((self.hostname, 80))

    def _request(self, method, path, *args, **kwargs):
        raw_response = kwargs.pop("raw_response", False)
        if path.startswith("/"):
            path = path[1:]
            assert not path.startswith("/")
        returned = requests.request(method, "http://{0}/{1}".format(self.hostname, path), *args, **kwargs)
        if raw_response:
            return returned

        returned.raise_for_status()
        return returned.json()

def _make_request_shortcut(method_name):
    def json_method(self, *args, **kwargs):
        return self._request(method_name, *args, **kwargs)

    json_method.__name__ = method_name
    setattr(Webapp, method_name, json_method)

    def raw_method(self, *args, **kwargs):
        return self._request(method_name, raw_response=True, *args, **kwargs)

    raw_method.__name__ = "{0}_raw".format(method_name)
    setattr(Webapp, raw_method.__name__, raw_method)

for _method in ("get", "put", "post", "delete"):
    _make_request_shortcut(_method)
