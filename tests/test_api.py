import requests

import pytest


@pytest.mark.parametrize('paged_url', ['sessions', 'tests', 'users'])
def test_pagination_cap(client, paged_url):
    url = client.api.url.add_path('rest').add_path(paged_url)
    for page_size, should_work in [
            (50, True),
            (2001, False),
            ]:
        resp = client.api.session.get(url.set_query_param('page_size', str(page_size)))
        if should_work:
            resp.raise_for_status()
        else:
            assert resp.status_code == requests.codes.bad_request
