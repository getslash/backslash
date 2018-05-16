import pytest


@pytest.mark.parametrize('use_spaces', [True, False])
def test_quick_search_subject(client, subjects, use_spaces):
    client.report_session_start(subjects=subjects)
    term = subjects[0]['name'][1:10]
    if use_spaces:
        term = ' {} '.format(term)
    res = client.api.call_function('quick_search', {'term': term})
    assert subjects[0]['name'] in {x['name'] for x in res if x['type'] == 'subject'}

@pytest.mark.parametrize('use_spaces', [True, False])
def test_quick_search_user(client, testuser_email, use_spaces):
    client.report_session_start() # quick search only searches users with existing sessions
    term = testuser_email.split('@')[0][-3:]
    if use_spaces:
        term = ' {} '.format(term)
    res = client.api.call_function('quick_search', {'term': term})
    assert testuser_email in {x['name'] for x in res if x['type'] == 'user'}
