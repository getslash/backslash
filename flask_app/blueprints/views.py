import os

from flask import send_from_directory, Blueprint, current_app
import sys

blueprint = Blueprint("views", __name__, template_folder="templates")

@blueprint.route("/")
def index():
    if not os.path.isdir(current_app.static_folder):
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'webapp', 'app'), 'index.html')
    return send_from_directory(current_app.static_folder, 'index.html')



################################################################################
