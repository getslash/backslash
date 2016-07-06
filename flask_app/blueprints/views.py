import os

import logbook

from flask import Blueprint, abort, current_app, send_from_directory

_logger = logbook.Logger(__name__)

blueprint = Blueprint("views", __name__, template_folder="templates")

_WEBAPP_ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'webapp', 'app')

@blueprint.route("/")
def index():
    return _send_static('index.html')

@blueprint.route("/styleguide")
def styleguide():
    if not current_app.config['DEBUG']:
        abort(404)
    return send_from_directory(_WEBAPP_ROOT, 'styleguide.html')


def _send_static(filename):
    if not os.path.isdir(current_app.static_folder):
        _logger.debug('Static folder {} does not exist', current_app.static_folder)
        folder = _WEBAPP_ROOT
    else:
        folder = current_app.static_folder
    _logger.debug('Serving {}/{}', folder, filename)
    return send_from_directory(folder, filename)



################################################################################
