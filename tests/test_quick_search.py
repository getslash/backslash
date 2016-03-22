def test_quick_search_subject(client, subjects):
    client.report_session_start(subjects=subjects)
    res = client.api.call_function('quick_search', {'term': subjects[0]['name'][1:10]})
    assert subjects[0]['name'] in {x['name'] for x in res if x['type'] == 'subject'}

def test_quick_search_user(client, testuser_email):
    term = testuser_email.split('@')[0][-3:]
    res = client.api.call_function('quick_search', {'term': term})
    assert testuser_email in {x['name'] for x in res if x['type'] == 'user'}
