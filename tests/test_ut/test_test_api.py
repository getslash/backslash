import flux
import pytest
import datetime

from .utils import raises_not_found, raises_conflict, raises_bad_request


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
    original_time = flux.current_timeline.time()
    test_time = started_test.start_time
    assert test_time == original_time


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


def test_test_duration(started_test):
    duration = 10
    start_time = started_test.start_time
    started_test.report_end(duration=duration)
    started_test.refresh()
    assert started_test.duration == duration


def test_end_test_doesnt_exist(nonexistent_test):
    with raises_not_found():
        nonexistent_test.report_end()


def test_add_error_nonexistent_test(nonexistent_test):
    with raises_not_found():
        nonexistent_test.add_error()


def test_add_failure_nonexistent_test(nonexistent_test):
    with raises_not_found():
        nonexistent_test.add_failure()


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
    assert started_test.status == 'FAILURE'


def test_get_status_skipped(started_test):
    started_test.add_failure()
    started_test.mark_skipped()
    started_test.report_end()
    started_test.refresh()
    assert started_test.status == 'SKIPPED'


@pytest.mark.parametrize('use_duration', [True, False])
def test_report_test_end(started_test, use_duration):
    if use_duration:
        started_test.report_end(duration=10)
    else:
        started_test.report_end()
    started_test.refresh()
    assert started_test.status == 'SUCCESS'


def test_add_metadata(started_test):
    metadata = {'logfile': '/var/log/foo'}
    started_test.add_metadata(metadata)
    started_test.refresh()
    assert started_test.test_metadata == metadata


def test_add_two_metadata_items(started_test):
    metadata1 = {'logfile': '/var/log/foo'}
    metadata2 = {'foo': 'bar'}
    metadata = dict(metadata1.items() + metadata2.items())
    started_test.add_metadata(metadata1)
    started_test.add_metadata(metadata2)
    started_test.refresh()
    assert started_test.test_metadata == metadata


def test_add_bad_metadata(started_test):
    with raises_bad_request():
        started_test.add_metadata('bad_metadata')


def test_add_metadata_nonexistent_test(nonexistent_test):
    with raises_not_found():
        nonexistent_test.add_metadata({'foo':'bar'})


