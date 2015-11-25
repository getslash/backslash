import math
import os
import sys
from uuid import uuid4

import logbook.compat
import requests

import flux
import pytest
from backslash import Backslash as BackslashClient
from flask.ext.loopback import FlaskLoopback
from flask_app import app, auth, models
from flask_app.utils.caching import cache
from munch import Munch
from urlobject import URLObject as URL

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def subjects():
    returned = [
        Munch(name='prod1', product='Car',
              version=None, revision='120'),
        Munch(name='prod2', product='Car',
              version='10', revision='1200'),
        Munch(name='prod3', product='Motorcycle',
              version='10', revision='1200'),
        Munch(name='prod4', product='Car',
              version=None, revision='120'),
    ]
    salt = '_{}'.format(uuid4())

    for subj in returned:
        subj.name += salt
        subj.product += salt
    return returned


@pytest.fixture(autouse=True, scope='session')
def freeze_timeline(request):

    original_factor = flux.current_timeline.get_time_factor()

    @request.addfinalizer
    def finalizer():
        flux.current_timeline.set_time_factor(original_factor)

    flux.current_timeline.set_time_factor(0)
    current_time = flux.current_timeline.time()
    next_round_time = math.ceil(current_time * 10000) / 10000.0
    flux.current_timeline.sleep(next_round_time - current_time)


@pytest.fixture(autouse=True, scope='function')
def advance_timeline():
    flux.current_timeline.sleep(10)


@pytest.fixture
def started_session(client):
    return client.report_session_start()


@pytest.fixture
def ended_session(client):
    # we don't use started_session to enable tests to use both...
    session = client.report_session_start()
    session.report_end()
    return session


@pytest.fixture
def nonexistent_session(client):
    from backslash.session import Session
    return Session(client, {'id': 238723287, 'type': 'session'})


@pytest.fixture
def started_test(started_session, file_name, class_name, test_name):
    return started_session.report_test_start(file_name=file_name, class_name=class_name, name=test_name, test_logical_id=str(uuid4()))


@pytest.fixture
def started_session_with_ended_test(started_session, test_info):
    test = started_session.report_test_start(
        test_logical_id=str(uuid4()), **test_info)
    test.report_end()
    return (started_session, test)


@pytest.fixture
def ended_test(started_session, test_info):
    returned = started_session.report_test_start(
        test_logical_id=str(uuid4()), **test_info)
    returned.report_end()
    return returned


@pytest.fixture
def nonexistent_test(client, started_session):
    from backslash.test import Test
    return Test(client, {'id': 6666, 'session_id': started_session.id, 'logical_id': '6677'})


@pytest.fixture
def logical_id():
    return 'my_logical_id'


@pytest.fixture
def error_data():
    data = {
        'exception': 'assert (2 + 2) == 5',
        'exception_type': 'AssertionError',
        'traceback': [{'filename': 'foo.py', 'lineno': 100, 'func_name': 'foo', 'locals': [], 'globals': [],
                          'code_line': 'line of code', 'code_string': 'lots of lines of code'},
                      {'filename': 'bar.py', 'lineno': 200, 'func_name': 'bar', 'locals': [], 'globals': [],
                          'code_line': 'line of code', 'code_string': 'lots of lines of code'}]
    }
    return data


@pytest.fixture
def metadata_key():
    return 'metadata_key'


@pytest.fixture(params=[1, 'hey', 2.0, True, None])
def metadata_value(request):
    return request.param


@pytest.fixture
def metadata():
    return {
        'key1': 'value1',
        'subobject': {
            'c': 20,
        }}


@pytest.fixture(params=['session', 'test'])
def metadata_holder(request, client, test_info):
    session = client.report_session_start(logical_id=str(uuid4()))
    if request.param == 'session':
        return session
    test = session.report_test_start(test_logical_id=str(uuid4()), **test_info)
    return test


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
    returned = BackslashClient(
        'http://{0}'.format(webapp_without_login.hostname), runtoken=runtoken)

    def _do_real_login():
        returned.api.session.post(
            returned.api.url.add_path('testing_login').add_query_param('user_id', str(testuser_id))).raise_for_status(),
    returned.do_real_login = _do_real_login
    return returned


@pytest.fixture
def real_login(client):
    client.do_real_login()


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
def runtoken(db, db_context, testuser):
    with db_context():
        token_string = str(uuid4())
        token = models.RunToken(user=testuser, token=token_string)
        db.session.add(token)
        db.session.commit()
    return token_string


def _get_role_fixture(role_name):

    def fixture(testuser_id, webapp_without_login):
        with webapp_without_login.app.app_context():
            user = models.User.query.get(testuser_id)
            user.roles.append(
                models.Role.query.filter_by(name=role_name).one())
            models.db.session.commit()
    fixture.__name__ = '{}_role'.format(role_name)
    return pytest.fixture(fixture)

moderator_role = _get_role_fixture('moderator')
proxy_role = _get_role_fixture('proxy')
admin_role = _get_role_fixture('admin')


@pytest.fixture
def testuser(testuser_tuple):
    return testuser_tuple[-1]


@pytest.fixture
def testuser_id(testuser_tuple):
    return testuser_tuple[0]


@pytest.fixture(scope='session')
def users_to_delete(request):
    returned = set()

    @request.addfinalizer
    def cleanup():
        with _create_flask_app().app_context():
            models.User.query.filter(models.User.id.in_(
                list(returned))).delete(synchronize_session=False)
            models.db.session.commit()
    return returned


def _create_user(users_to_delete):
    user = models.User(email='user{}@localhost'.format(uuid4()), active=True)
    models.db.session.add(user)
    models.db.session.commit()
    user_id = user.id
    users_to_delete.add(user_id)
    return user.id, user.email, user


@pytest.fixture
def testuser_email(testuser_tuple):
    return testuser_tuple[1]


@pytest.fixture
def otheruser_email(otheruser_tuple):
    return otheruser_tuple[1]


@pytest.fixture
def otheruser_id(otheruser_tuple):
    return otheruser_tuple[0]


@pytest.fixture
def testuser_tuple(db_context, users_to_delete):
    with db_context():
        return _create_user(users_to_delete)


@pytest.fixture
def otheruser_tuple(db_context, users_to_delete):
    with db_context():
        return _create_user(users_to_delete)


@pytest.fixture
def db_context(webapp_without_login):
    return webapp_without_login.app.app_context


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
    return _get_api_object_by_typename(client=client, typename=request.param)


@pytest.fixture(params=['session', 'test'])
def warning_container(request, client):
    return _get_api_object_by_typename(typename=request.param, client=client)


def _get_api_object_by_typename(*, typename, client):
    session = client.report_session_start()
    if typename == 'session':
        return session
    elif typename == 'test':
        test = session.report_test_start('name')
        return test
    raise NotImplementedError()  # pragma: no cover


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
        self.hostname = str(uuid4())
        self.url = URL('http://{0}'.format(self.hostname))

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


@pytest.fixture(params=['admin', 'proxy', 'moderator'])
def role(request):
    return request.param
