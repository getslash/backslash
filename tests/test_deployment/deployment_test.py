from unittest import TestCase
import os
import requests
from ..test_utils import config_utils
from urlobject import URLObject

class DeploymentTest(TestCase):
    def setUp(self):
        super(DeploymentTest, self).setUp()
        self.www_port = config_utils.get_config_int("www_port", 8080)
    def request(self, method, path, *args, **kwargs):
        url = URLObject("http://127.0.0.1").with_port(self.www_port).with_path(path)
        return requests.request(method, url, *args, **kwargs)
