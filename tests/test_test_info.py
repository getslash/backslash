
def test_tests_by_info(client, started_session, file_name, class_name, test_name):
    def _report_start():
        return started_session.report_test_start(file_name=file_name, class_name=class_name, name=test_name)

    tests = []
    num_tests = 10
    for _ in range(num_tests):
        t = _report_start()
        t.report_end()
        tests.append(t)

    test_info_id = tests[0].test_info_id
    assert {t.test_info_id for t in tests} == {test_info_id}
    assert tests[0].test_info_id is not None

    unrelated = started_session.report_test_start(file_name=file_name, class_name=class_name, name=test_name + 'x')
    assert unrelated.test_info_id != test_info_id

    retrieved = client.query('rest/tests', query_params={'info_id': test_info_id}).all()

    assert {test_info_id} == {t.test_info_id for t in retrieved}
    assert {t.id for t in tests} == {t.id for t in retrieved}


def test_get_info_directly(client, started_session, file_name, class_name, test_name):
    test = started_session.report_test_start(file_name=file_name, class_name=class_name, name=test_name)

    info = client.api.get('rest/test_infos/{}'.format(test.test_info_id))
    assert info['file_name'] == file_name
    assert info['class_name'] == class_name
    assert info['name'] == test_name
