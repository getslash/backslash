import pytest


def test_session_status_is_running_by_default(started_session):
    assert started_session.refresh().status == 'RUNNING'


@pytest.mark.parametrize('with_failure', [True, False])
@pytest.mark.parametrize('with_error', [True, False])
def test_test_status_is_running_if_not_finished(started_test, with_error, with_failure):
    if with_error:
        started_test.add_error('SomeException', 'SomeType')
    if with_failure:
        pytest.skip('n/i')
    assert started_test.refresh().status == 'RUNNING'


def test_add_error_doesnt_affect_error_count_until_finished(started_session, started_test):
    assert started_session.refresh().num_error_tests == 0
    started_test.add_error('E', 'T')
    assert started_session.refresh().num_error_tests == 0
    assert started_test.refresh().num_errors == 1
    started_test.report_end()
    assert started_session.refresh().num_error_tests == 1


def test_multiple_errors_counted_as_one(started_session, started_test):
    for i in range(5):
        started_test.add_error('E{}'.format(i), 'T{}'.format(i))
    assert started_session.refresh().num_error_tests == 0
    assert started_test.refresh().num_errors == 5
    started_test.report_end()
    assert started_session.refresh().num_error_tests == 1

