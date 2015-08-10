import os
import sys
import uuid
from uuid import uuid4

import requests
from flask.ext.loopback import FlaskLoopback
from urlobject import URLObject as URL

import pytest
from backslash import Backslash as BackslashClient
import logbook.compat
from flask_app import app, models
from flask_app.utils.caching import cache

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture(scope='session', autouse=True)
def patch_proxy_bypass():
    """Work around a bug causing should_bypass_proxies to take forever when VPN is active
    """
    import requests
    requests.utils.should_bypass_proxies = lambda url: True

@pytest.fixture(scope='session', autouse=True)
def invalidate_cache():
    cache.invalidate()


def pytest_addoption(parser):
    parser.addoption("--url", action="store", default=None)


@pytest.fixture(scope='session', autouse=True)
def redirect_logging():
    logbook.compat.redirect_logging()


@pytest.fixture
def client(webapp_without_login, runtoken, testuser_id):
    returned = BackslashClient('http://{0}'.format(webapp_without_login.hostname), runtoken=runtoken)
    def _do_real_login():
        returned.api.session.post(
            returned.api.url.add_path('testing_login').add_query_param('user_id', str(testuser_id))).raise_for_status(),
    returned.do_real_login = _do_real_login
    return returned


@pytest.fixture
def backslash_url(request):
    url = request.config.getoption("--url")
    if url is None:
        pytest.skip()
    return URL(url)


@pytest.fixture
def webapp(testuser, request):
    returned = _create_webapp(request)
    returned.post('/testing_login')
    return returned


@pytest.fixture
def webapp_without_login(request):
    return _create_webapp(request)


_cached_app = None
_cached_config = None

def _create_flask_app():
    global _cached_app
    global _cached_config

    if _cached_app is None:

        returned = _cached_app = app.create_app({
            #'SQLALCHEMY_DATABASE_URI': 'postgresql://127.0.0.1/backslash-ut',
            'SECRET_KEY': 'testing-key',
            'TESTING': True,
            'SECURITY_PASSWORD_SALT': 'testing_salt',
            'JSONIFY_PRETTYPRINT_REGULAR': False,
            'JSON_SORT_KEYS': False,
        })
        _cached_config = returned.config.copy()
        returned.extensions['security'].password_salt = returned.config[
            'SECURITY_PASSWORD_SALT']

    else:
        returned = _cached_app
        returned.config.update(_cached_config.copy())
    return returned


def _create_webapp(request):
    returned = Webapp(_create_flask_app())
    returned.activate()
    request.addfinalizer(returned.deactivate)
    return returned

@pytest.fixture
def db():
    return models.db

@pytest.fixture
def runtoken(db, webapp_without_login, testuser):
    with webapp_without_login.app.app_context():
        token_string = str(uuid4())
        token = models.RunToken(user=testuser, token=token_string)
        db.session.add(token)
        db.session.commit()
    return token_string

@pytest.fixture
def testuser(testuser_and_id):
    return testuser_and_id[0]

@pytest.fixture
def testuser_id(testuser_and_id):
    return testuser_and_id[1]

@pytest.fixture(scope='session')
def users_to_delete(request):
    returned = set()
    @request.addfinalizer
    def cleanup():
        with _create_flask_app().app_context():
            models.User.query.filter(models.User.id.in_(list(returned))).delete(synchronize_session=False)
            models.db.session.commit()
    return returned

@pytest.fixture
def testuser_and_id(request, db, webapp_without_login, testuser_email, users_to_delete):
    with webapp_without_login.app.app_context():
        user = models.User(email=testuser_email, active=True)
        db.session.add(user)
        db.session.commit()
        user_id = user.id
        users_to_delete.add(user_id)
    return user, user_id

@pytest.fixture
def testuser_email():
    return 'testing{}@localhost'.format(uuid4())


@pytest.fixture
def file_name():
    return 'path/to/test/file.py'


@pytest.fixture(params=['SomeClass', None])
def class_name(request):
    return request.param


@pytest.fixture
def test_name():
    return 'test_something'


@pytest.fixture
def test_info(file_name, test_name, class_name):
    return {'file_name': file_name, 'name': test_name, 'class_name': class_name}

@pytest.fixture(params=['session', 'test'])
def error_container(request, client):
    session = client.report_session_start()
    if request.param == 'session':
        return session
    elif request.param == 'test':
        test = session.report_test_start('name')
        return test
    raise NotImplementedError() # pragma: no cover

@pytest.fixture
def nonexistent_error_container(error_container):
    new_data = error_container._data.copy()
    new_data['id'] *= 2
    returned = type(error_container)(error_container.client, new_data)
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
        raw_response = kwargs.pop("raw_response", False)
        if path.startswith("/"):
            path = path[1:]
            assert not path.startswith("/")
        returned = requests.request(
            method, "http://{0}/{1}".format(self.hostname, path), *args, **kwargs)
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


@pytest.fixture
def flask_app(webapp):
    return webapp.app
