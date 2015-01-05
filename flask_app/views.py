from flask import render_template
import sys

from .app import app


@app.route("/")
def index():
    return render_template("index.html", version=sys.version)
