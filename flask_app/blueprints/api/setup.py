import json

import requests

from flask import abort
from flask_security.utils import encrypt_password
from flask_simple_api import error_abort
import logbook
from sqlalchemy.exc import IntegrityError

from .blueprint import API
from ... import models
from ...config import get_runtime_config_public_dict, get_runtime_config_private_dict
from ...auth import user_datastore
from ...models import db


_logger = logbook.Logger(__name__)


@API(generates_activity=False, require_login=False)
def get_app_config():
    return get_runtime_config_public_dict()

_DEFAULTS = {
    'default_domain': None,
    'google_oauth2_enabled': False,
    'google_oauth2_client_id': None,
    'google_oauth2_client_secret': None,
    'ldap_login_enabled': False,
    'ldap_uri': None,
    'ldap_base_dn': None,
}

@API(generates_activity=False, require_login=False)
def setup(config: dict):
    if not get_runtime_config_private_dict()['setup_needed']:
        error_abort('Setup already performed', code=requests.codes.conflict)

    unified_config = _DEFAULTS.copy()
    unified_config.update({key: value for key, value in config.items() if key in _DEFAULTS})
    unified_config['setup_needed'] = False
    #known preferences
    for key, value in unified_config.items():
        db.session.execute('''
        INSERT INTO app_config (key, value) VALUES (:key, :value)
        ON CONFLICT(key) DO NOTHING
        ''', {'key': key, 'value': json.dumps(value)})
    db.session.commit()


    # admin user
    admin_user_email = config.get('admin_user_email')
    admin_user_password = config.get('admin_user_password')
    if admin_user_email and admin_user_password and not db.session.query(models.roles_users).count():
        try:
            user = user_datastore.create_user(
                active=True,
                password=encrypt_password(admin_user_password),
                email=admin_user_email,
            )
            user_datastore.add_role_to_user(user, 'admin')
            db.session.commit()
        except IntegrityError:
            _logger.debug('User already exists. Skipping admin user creation')
