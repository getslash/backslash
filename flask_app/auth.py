import ldap
import logbook
import requests
from flask import (abort, Blueprint, current_app, jsonify, request)
from flask_security import SQLAlchemyUserDatastore
from itsdangerous import BadSignature, TimedSerializer

from flask_login import logout_user
from flask_simple_api import error_abort
from flask_security.utils import login_user, verify_password

from .config import get_runtime_config_private_dict
from .models import db, Role, User
from .utils.oauth2 import get_oauth2_identity

_logger = logbook.Logger(__name__)

_MAX_TOKEN_AGE = 60 * 60 * 24 * 30  # one month

auth = Blueprint("auth", __name__, template_folder="templates")

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)


@auth.route('/testing_login', methods=['POST'])
def testing_login():
    if not current_app.config.get('TESTING'):
        abort(requests.codes.not_found)

    user_id = request.args.get('user_id')
    if user_id is not None:
        user = User.query.get_or_404(int(user_id))
    else:
        testing_email = 'testing@localhost'
        user = get_or_create_user({'email': testing_email})
    assert user
    login_user(user)
    user_info = {}
    return _make_success_login_response(user, user_info)


@auth.route("/login", methods=['POST'])
def login():

    credentials = request.get_json(silent=True)
    if not isinstance(credentials, dict):
        error_abort('Credentials provided are not a JSON object')

    if credentials.get('username'):
        return _login_with_credentials(credentials)

    auth_code = credentials.get('authorizationCode')
    if auth_code:
        return _login_with_google_oauth2(auth_code)

    error_abort('No credentials were specified', code=requests.codes.unauthorized)


def _login_with_credentials(credentials):
    config = get_runtime_config_private_dict()
    username = credentials.get('username')
    password = credentials.get('password')

    email = _fix_email(username, config)
    user = User.query.filter_by(email=email).first()

    if user is not None and user.password and verify_password(password, user.password):
        login_user(user)
        return _make_success_login_response(user)
    _logger.debug('Could not login user locally (no user or password mismatch)')
    return _login_with_ldap(email, password, config)

def _fix_email(email, runtime_config):
    if email:
        domain = runtime_config['default_domain']
        if domain and not domain.startswith('@'):
            domain = '@' + domain
        if '@' not in email and domain:
            email += domain
    return email


def _login_with_ldap(email, password, config):
    _logger.debug('Attempting login via LDAP for {}...', email)

    _login_failed = functools.partial(
        error_abort,
        'Username or password are incorrect for {}'.format(email), code=requests.codes.unauthorized)

    if not config['ldap_login_enabled'] or not email or not password:
        _logger.debug('Rejecting login because LDAP is disabled or no username/password')
        _login_failed()

    try:

        ldap_obj = ldap.initialize(config['ldap_uri'])
        ldap_obj.bind_s(email, password)
        ldap_infos = ldap_obj.search_s(config['ldap_base_dn'], ldap.SCOPE_SUBTREE, 'userPrincipalName={}'.format(email))
        if not ldap_infos:
            _logger.error('Could not authenticate via LDAP - no records found')
            _login_failed()

        ldap_info = ldap_infos[0][1]
        user_info = {
            'email': ldap_info['mail'][0].decode('utf-8'),
            'given_name': ldap_info['givenName'][0].decode('utf-8'),
            'family_name': ldap_info['sn'][0].decode('utf-8'),
        }
        user = get_or_create_user(user_info)
        login_user(user)
        return _make_success_login_response(user, user_info)
    except ldap.INVALID_CREDENTIALS:
        _logger.error('LDAP Invalid credentials', exc_info=True)
        _login_failed()


def _login_with_google_oauth2(auth_code):
    user_info = get_oauth2_identity(auth_code)
    if not user_info:
        error_abort('Could not complete OAuth2 exchange', code=requests.codes.unauthorized)

    _check_alowed_email_domain(user_info)

    user = get_or_create_user(user_info)
    login_user(user)

    return _make_success_login_response(user, user_info)


@auth.route("/logout", methods=['POST'])
def logout():
    logout_user()
    return jsonify({})


def _make_success_login_response(user, user_info=None):
    if user_info is None:
        user_info = {'email': user.email, 'given_name': user.first_name, 'last_name': user.last_name}
    token = _generate_token(user, user_info)
    _logger.debug('OAuth2 login success for {}. Token: {!r}', user_info, token)

    return jsonify({
        'auth_token': token,
        'user_info': user_info,
    })


@auth.route("/reauth", methods=['POST'])
def reauth():
    token = (request.json or {}).get('auth_token')
    if token is None:
        error_abort('Missing reauth token')
    try:
        token_data = _get_token_serializer().loads(
            token, max_age=_MAX_TOKEN_AGE)
    except BadSignature:
        error_abort('Reauth token invalid', code=requests.codes.unauthorized)
    user = User.query.get_or_404(token_data['user_id'])

    login_user(user)

    return jsonify({
        'auth_token': token,
        'user_info': token_data['user_info'],
    })


def _generate_token(user, user_info):
    return _get_token_serializer().dumps({
        'user_id': user.id,
        'user_info': user_info})


def _get_token_serializer():
    return TimedSerializer(current_app.config['SECRET_KEY'])


def get_or_create_user(user_info):
    email = user_info['email']
    user = user_datastore.get_user(email)
    if not user:
        user = user_datastore.create_user(
            active=True,
            email=email)
        user_datastore.db.session.commit()

    if user.first_name is None:
        user.first_name = user_info.get('given_name', user_info.get('first_name'))
        user.last_name = user_info.get('family_name', user_info.get('last_name'))
        user_datastore.db.session.commit()

    user_info['user_id'] = user.id
    user_info['roles'] = [role.name for role in user.roles]
    user_info['can'] = {role.name: True for role in user.roles}
    user_info['can']['moderate'] = user_info['can'].get('moderator', False)

    _logger.debug('User info: {}', user_info)

    return user


def _check_alowed_email_domain(user_info):
    email = user_info['email']
    domain = email.split('@', 1)
    allowed = current_app.config.get('ALLOWED_EMAIL_DOMAINS')
    if allowed is None:
        return
    if domain not in allowed:
        error_abort('Disallowed email domain for {}'.format(email), code=requests.codes.unauthorized)
