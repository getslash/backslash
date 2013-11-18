import httplib
import os
import sys
import unittest

from flask_app import app

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

class TestCase(unittest.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.app = app.app.test_client()
        app.app.config["SECRET_KEY"] = "testing_key"

def _make_request_shortcut(method):
    def shortcut(self, *args, **kwargs):
        returned = getattr(self.app, method)(*args, **kwargs)
        if returned.status_code not in (httplib.OK, httplib.CREATED):
            msg = "HTTP {} {}: Error {}".format(method.upper(), args[0], returned.status_code)
            self.fail(msg)
        return returned

    shortcut_name = shortcut.__name__ = "_{}".format(method)
    setattr(TestCase, shortcut_name, shortcut)

for _method in ("get", "put", "post", "delete"):
    _make_request_shortcut(_method)
