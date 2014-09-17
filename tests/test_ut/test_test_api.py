import flux
import pytest

from .utils import raises_not_found, raises_conflict


def test_report_test_start(started_session, test_name):
    test = started_session.report_test_start(name=test_name)
    assert test is not None

def test_report_test_start_logical_id(started_session, test_name):
    test = started_session.report_test_start(name=test_name, test_logical_id='11')
    assert test is not None


def test_test_session_id(started_session, started_test):
    assert started_test.session_id == started_session.id


def test_cannot_start_test_ended_session(ended_session):
    with raises_conflict():
        ended_session.report_test_start(name='name')


def test_cannot_start_test_nonexistent_session(nonexistent_session):
    with raises_not_found():
        nonexistent_session.report_test_start(name='name')


def test_start_time(started_test):
    assert abs(started_test.start_time - flux.current_timeline.time()) < 0.0001


def test_duration_empty(started_test):
    assert started_test.duration is None


def test_duration(started_test):
    duration = 10.5
    flux.current_timeline.sleep(duration)
    started_test.report_end()
    started_test.refresh()
    assert started_test.duration == duration


@pytest.mark.parametrize('use_duration', [True, False])
def test_report_test_end(started_test, use_duration):
    duration = 10
    start_time = started_test.start_time
    if use_duration:
        started_test.report_end(duration=duration)
    else:
        flux.current_timeline.sleep(10)
        started_test.report_end()
    started_test.refresh()
    assert started_test.end_time == start_time + duration


def test_end_test_doesnt_exist(nonexistent_test):
    with raises_not_found():
        nonexistent_test.report_end()


def test_end_test_twice(ended_test):
    with raises_conflict():
        ended_test.report_end()

def test_test_add_error(started_test):
    started_test.add_error()
    started_test.refresh()
    assert started_test.num_errors == 1

def test_test_add_failure(started_test):
    started_test.add_failure()
    started_test.refresh()
    assert started_test.num_failures == 1

def test_get_status_running(started_test):
    started_test.refresh() #probably not needed
    assert started_test.status == 'RUNNING'

def test_get_status_error(started_test):
    started_test.add_error()
    started_test.report_end()
    started_test.refresh()
    assert started_test.status == 'ERROR'

def test_get_status_failure(started_test):
    started_test.add_failure()
    started_test.report_end()
    started_test.refresh()
    assert started_test.status == 'FAILED'

def test_get_status_skipped(started_test):
    started_test.add_failure()
    started_test.report_end(skipped=True)
    started_test.refresh()
    assert started_test.status == 'SKIPPED'

@pytest.mark.parametrize('use_duration', [True, False])
def test_report_test_end(started_test, use_duration):
    if use_duration:
        started_test.report_end(duration=10)
    else:
        started_test.report_end()
    started_test.refresh()
    assert started_test.status == 'PASSED'

