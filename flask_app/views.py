from flask import render_template, Blueprint
import sys


views = Blueprint("views", __name__, template_folder="templates")

@views.route("/")
def index():
    return render_template("index.html", version=sys.version)
