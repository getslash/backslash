import pytest


def test_search_by_product_name(client, sessions, session_to_find, product_info):
    [session] = client.query_sessions().filter(product_name=product_info['name'])
    assert session == session_to_find

@pytest.fixture
def session_to_find(client, product_info):
    session = client.report_session_start()
    session.set_product(**product_info)
    session.report_end()
    session.refresh()
    return session


@pytest.fixture
def sessions(client):
    num_sessions = 3
    for i in range(num_sessions):
        s = client.report_session_start()
        s.report_end()
    assert len(client.query_sessions()) == num_sessions
