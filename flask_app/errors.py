from .app import app

from flask import render_template, make_response

def _define_custom_error_page(code):
    @app.errorhandler(code)
    def _handler(err):
        return make_response(render_template("errors/{}.html".format(code)), code)

_define_custom_error_page(500)
_define_custom_error_page(404)
_define_custom_error_page(403)
