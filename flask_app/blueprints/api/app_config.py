from flask import current_app

from .blueprint import API


@API(generates_activity=False, require_login=False)
def get_app_config():
    return {
        'debug': current_app.config['DEBUG'],
        'oauth2_client_id': current_app.config.get('OAUTH2_CLIENT_ID'),
    }
