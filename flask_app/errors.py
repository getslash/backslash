from .app import app
from flask import render_template

def _define_custom_error_page(code):
    @app.errorhandler(code)
    def _handler(err):
        return render_template("errors/{}.html".format(code))

_define_custom_error_page(500)
_define_custom_error_page(404)
_define_custom_error_page(403)
