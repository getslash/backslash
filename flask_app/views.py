import os

from flask import send_from_directory

from .app import app


@app.route("/")
def index():
    if not os.path.isdir(app.static_folder):
        return send_from_directory(os.path.join(os.path.dirname(__file__), '..', 'webapp', 'app'), 'index.html')
    return send_from_directory(app.static_folder, 'index.html')
