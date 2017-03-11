import os

import logbook

from flask import Blueprint, abort, current_app, send_from_directory

_logger = logbook.Logger(__name__)

blueprint = Blueprint("views", __name__, template_folder="templates")

_WEBAPP_ROOT = os.path.join(os.path.dirname(__file__), '..', '..', 'webapp', 'dist')

@blueprint.route("/")
def index():
    return send_from_directory(_WEBAPP_ROOT, 'index.html')


@blueprint.route('/static/<path:filename>')
def serve_static(filename): # pylint: disable=unused-variable
    return send_from_directory(_WEBAPP_ROOT, filename)


@blueprint.route("/styleguide")
def styleguide():
    if not current_app.config['DEBUG']:
        abort(404)
    return send_from_directory(_WEBAPP_ROOT, 'styleguide.html')



################################################################################
