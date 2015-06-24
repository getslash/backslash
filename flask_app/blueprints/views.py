import os

from flask import send_from_directory, Blueprint, current_app
import sys
import logbook

_logger = logbook.Logger(__name__)

blueprint = Blueprint("views", __name__, template_folder="templates")

@blueprint.route("/")
def index():
    if not os.path.isdir(current_app.static_folder):
        _logger.debug('Static folder {} does not exist', current_app.static_folder)
        folder = os.path.join(os.path.dirname(__file__), '..', 'webapp', 'app')
    else:
        folder = current_app.static_folder
    _logger.debug('Serving {}/index.html', folder)
    return send_from_directory(folder, 'index.html')



################################################################################
