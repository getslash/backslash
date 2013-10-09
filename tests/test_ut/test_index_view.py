from ..test_utils import TestCase

class IndexViewTest(TestCase):
    def test_index_view(self):
        rv = self.app.get("/")

