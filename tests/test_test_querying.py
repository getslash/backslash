import requests

def test_test_parameters(client, started_session):
    tests = []
    for i in range(10):
        test = started_session.report_test_start(name='test{}'.format(i)).refresh()
        test.report_end()
        tests.append(test)

    def get_test(**kwargs):
        resp = requests.get(client.api.url.add_path('rest/tests'), params={'session_id': started_session.id, **kwargs})
        resp.raise_for_status()
        tests = resp.json()['tests']
        assert len(tests) == 1
        return tests[0]

    assert get_test(after_index=tests[2].test_index)['id'] == tests[3].id
    assert get_test(before_index=tests[5].test_index)['id'] == tests[4].id
