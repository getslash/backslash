from yarl import URL
from flask import current_app
from . import models
try:
    from .__version__ import __version__
except ImportError:
    import subprocess
    status, output = subprocess.getstatusoutput('git describe --tags')
    if status == 0:
        __version__ = output.strip()
    else:
        __version__ = '?.?.?'


def get_runtime_config_private_dict():
    returned = {
        'debug': current_app.config['DEBUG'],
        'version': __version__,
        'setup_needed': True,
        **{
            key: current_app.config[key]
            for key in (
                    'display_names',
                    'test_metadata_links',
                    'session_metadata_display_items',
                    'test_metadata_display_items',
            )
        }
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
