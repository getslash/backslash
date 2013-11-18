import httplib

from ..test_utils import TestCase

class IndexViewTest(TestCase):

    def test_index_view(self):
        rv = self.app.get("/")

    def test_not_found_errors(self):
        rv = self.app.get("/nonexistent_path")
        self.assertEquals(rv.status_code, httplib.NOT_FOUND)

