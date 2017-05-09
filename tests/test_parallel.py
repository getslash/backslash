from uuid import uuid4
import requests
import pytest

def get_test(client, session_id):
    resp = requests.get(client.api.url.add_path('rest/tests'), params={'session_id': session_id})
    resp.raise_for_status()
    tests = resp.json()['tests']
    assert len(tests) == 1
    return tests[0]


def get_sessions(client, params):
    resp = requests.get(client.api.url.add_path('rest/sessions'), params=params)
    resp.raise_for_status()
    sessions = resp.json()['sessions']
    return sessions


def test_getting_tests_of_parent(started_parallel_session, test_info, client):
    (parent_session, child_session) = started_parallel_session
    test = child_session.report_test_start(test_logical_id=str(uuid4()), **test_info)
    test.report_end()
    returned_test = get_test(client, parent_session.id)
    assert returned_test['id'] == test.id


def test_child_not_in_sessions_list(started_parallel_session, client):
    (parent_session, child_session) = started_parallel_session
    sessions = get_sessions(client, None)
    session_ids = [session['id'] for session in sessions]
    assert parent_session.id in session_ids
    assert child_session.id not in session_ids


def test_child_in_sessions_when_query_parent_logical_id(client):
    parent_logical_id = str(uuid4())
    child_logical_id = str(uuid4())
    parent_session = client.report_session_start(logical_id=parent_logical_id)
    assert parent_session
    child_session = client.report_session_start(parent_logical_id=parent_logical_id, logical_id=child_logical_id)
    assert child_session
    sessions = get_sessions(client, {'parent_logical_id':parent_logical_id})
    assert len(sessions) == 1
    assert child_session.id == sessions[0]['id']


def test_parent_logical_id_not_found(client):
    parent_logical_id = str(uuid4())
    wrong_parent_logical_id = str(uuid4())
    child_logical_id = str(uuid4())
    parent_session = client.report_session_start(logical_id=parent_logical_id)
    assert parent_session
    with pytest.raises(requests.HTTPError):
        child_session = client.report_session_start(parent_logical_id=wrong_parent_logical_id, logical_id=child_logical_id)


def test_duplicate_logic_id(client):
    parent_logical_id = str(uuid4())
    parent_session = client.report_session_start(logical_id=parent_logical_id)
    assert parent_session
    with pytest.raises(requests.HTTPError):
        child_session = client.report_session_start(logical_id=parent_logical_id)


def test_session_counts(started_parallel_session, test_info):
    (parent_session, child_session) = started_parallel_session
    counts = {
        'num_failed_tests': 3,
        'num_error_tests': 2,
        'num_skipped_tests': 4,
        'num_finished_tests': 16,
    }

    remaining = counts.copy()
    while remaining['num_finished_tests']:
        remaining['num_finished_tests'] -= 1

        test = child_session.report_test_start(**test_info)

        if remaining['num_failed_tests']:
            test.add_failure('F')
            remaining['num_failed_tests'] -= 1
        elif remaining['num_error_tests']:
            test.add_error('E')
            remaining['num_error_tests'] -= 1
        elif remaining['num_skipped_tests']:
            test.mark_skipped()
            remaining['num_skipped_tests'] -= 1

        test.report_end()

    child_session.report_end()
    parent_session.report_end()
    child_session.refresh()
    parent_session.refresh()

    for key, value in counts.items():
        assert getattr(parent_session, key) == value
        assert getattr(child_session, key) == value
