import sys
import os
import requests
import unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src import app

class TestCase(unittest.TestCase):
    def setUp(self):
        super(TestCase, self).setUp()
        self.app = app.app.test_client()
        app.app.config["SECRET_KEY"] = "testing_key"
