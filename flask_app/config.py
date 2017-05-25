from flask import current_app
from . import models
from .__version__ import __version__


def get_runtime_config_private_dict():
    returned = {
        'debug': current_app.config['DEBUG'],
        'version': __version__,
        'setup_needed': True,
        'display_names': current_app.config['display_names'],
    }
    returned.update(
        (cfg.key, cfg.value)
        for cfg in models.AppConfig.query.all()
    )
    return returned


def get_runtime_config_public_dict():
    returned = get_runtime_config_private_dict()
    for key in list(returned):
        if 'secret' in key.lower():
            returned.pop(key)
    return returned
