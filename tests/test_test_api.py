import flux
import pytest

from sentinels import NOTHING

from .utils import raises_not_found, raises_conflict


def test_test_information_filename(started_test, file_name):
    assert started_test.info['file_name'] == file_name


def test_test_information_classname(started_test, class_name):
    assert started_test.info['class_name'] == class_name


def test_test_information_name(started_test, test_name):
    assert started_test.info['name'] == test_name





def test_report_test_start_logical_id(started_session, test_name):
    test = started_session.report_test_start(
        name=test_name, test_logical_id='11')
    assert test is not None


def test_report_interactive_test_start(client):
    num_tests = 10
    session = client.report_session_start(total_num_tests=num_tests)
    assert session.total_num_tests == num_tests
    t = session.report_test_start('<interactive>', is_interactive=True)
    assert t.refresh().is_interactive == True
    assert session.refresh().total_num_tests == num_tests + 1


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


def test_end_test_twice(ended_test):
    with raises_conflict():
        ended_test.report_end()


def test_test_add_error(started_test):
    started_test.add_error('E')
    started_test.refresh()
    assert started_test.num_errors == 1


def test_get_status_running(started_test):
    started_test.refresh()  # probably not needed
    assert started_test.status == 'RUNNING'


def test_get_status_error(started_test):
    started_test.add_error('E')
    started_test.report_end()
    started_test.refresh()
    assert started_test.status == 'ERROR'


def test_get_status_failure(started_test):
    started_test.add_failure('F')
    started_test.report_end()
    started_test.refresh()
    assert started_test.status == 'FAILURE'


def test_first_error(started_test):
    for i in range(3):
        flux.current_timeline.sleep(1)
        started_test.add_error(str(i))
    started_test.refresh()
    assert started_test.first_error['message'] == '0'


def test_get_status_skipped(started_test):
    started_test.mark_skipped()
    started_test.report_end()
    started_test.refresh()
    assert started_test.status == 'SKIPPED'


def test_get_status_skipped_and_failure(started_test):
    started_test.add_failure('F')
    started_test.mark_skipped()
    started_test.report_end()
    started_test.refresh()
    assert started_test.status == 'FAILURE'


@pytest.mark.parametrize('use_duration', [True, False])
def test_report_test_end(started_test, use_duration):
    if use_duration:
        started_test.report_end(duration=10)
    else:
        started_test.report_end()
    started_test.refresh()
    assert started_test.status == 'SUCCESS'


@pytest.mark.parametrize('reason', [None, 'some reason here'])
def test_skip_reason(started_test, reason):
    started_test.mark_skipped(reason=reason)
    started_test.report_end()
    assert started_test.refresh().status == 'SKIPPED'
    assert started_test.skip_reason == reason


def test_test_variation(started_session, variation, test_name, class_name):
    test = started_session.report_test_start(
        name=test_name, class_name=class_name, variation=variation)
    if variation is NOTHING:
        expected_variation = None
    else:
        expected_variation = variation
    assert test.refresh().variation == expected_variation


def test_test_variation_invalid_values(started_session, invalid_variation, test_name, class_name):
    test = started_session.report_test_start(
        name=test_name, class_name=class_name, variation=invalid_variation)
    assert test.refresh().variation != invalid_variation
    assert test.variation # make sure it is not empty


def test_test_start_with_metadata(started_session, test_name, class_name):
    metadata = {'metadata_key1': 'metadata_value1',
                'metadata_key2': 'metadata_value2'}
    test = started_session.report_test_start(
        name=test_name, class_name=class_name, metadata=metadata)
    assert test.refresh().get_metadata() == metadata
