import os
import sys
import uuid

import requests
from flask.ext.loopback import FlaskLoopback
from urlobject import URLObject as URL

import pytest
from flask_app import app

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def pytest_addoption(parser):
    parser.addoption("--www-port", action="store", default=8080, type=int)

@pytest.fixture
def webapp_path(request):
    port = request.config.getoption("--www-port")
    return URL("http://127.0.0.1").with_port(port)

@pytest.fixture
def webapp(request):
    returned = Webapp(app.app)
    returned.app.config["SECRET_KEY"] = "testing_key"
    returned.app.config["TESTING"] = True
    returned.activate()
    request.addfinalizer(returned.deactivate)
    return returned


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
        if path.startswith("/"):
            path = path[1:]
            assert not path.startswith("/")
        return requests.request(method, "http://{0}/{1}".format(self.hostname, path), *args, **kwargs)

    def get(self, *args, **kwargs):
        return self._request("get", *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._request("post", *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._request("delete", *args, **kwargs)

    def put(self, *args, **kwargs):
        return self._request("put", *args, **kwargs)
