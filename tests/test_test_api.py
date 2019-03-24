import flux
import pytest

from sentinels import NOTHING
from uuid import uuid4

from .utils import raises_not_found, raises_conflict


def test_test_information_filename(started_test, file_name):
    assert started_test.info['file_name'] == file_name


def test_test_status_description(started_test):
    assert started_test.status_description is None
    description = 'blap'
    started_test.update_status_description(description)
    assert started_test.refresh().status_description == description
    started_test.report_end()
    assert started_test.refresh().status_description is None


def test_test_information_classname(started_test, class_name):
    assert started_test.info['class_name'] == class_name


def test_test_information_name(started_test, test_name):
    assert started_test.info['name'] == test_name


def test_report_test_start_logical_id(started_session, test_name):
    test = started_session.report_test_start(
        name=test_name, test_logical_id='11')
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


def test_end_test_twice(ended_test):
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
        name=test_name, class_name=class_name, variation=variation, test_logical_id=str(uuid4()))
    if variation is NOTHING:
        expected_variation = None
    else:
        expected_variation = variation
    assert test.refresh().variation == expected_variation


def test_test_variation_invalid_values(started_session, invalid_variation, test_name, class_name):
    test = started_session.report_test_start(
        name=test_name,
        class_name=class_name,
        variation=invalid_variation,
        test_logical_id=str(uuid4()))
    assert test.refresh().variation != invalid_variation
    assert test.variation # make sure it is not empty


def test_test_start_with_metadata(started_session, test_name, class_name):
    metadata = {'metadata_key1': 'metadata_value1',
                'metadata_key2': 'metadata_value2'}
    test = started_session.report_test_start(
        name=test_name, class_name=class_name, metadata=metadata)
    assert test.refresh().get_metadata() == metadata


def test_test_index_default(started_session, test_name):
    test_1 = started_session.report_test_start(name=test_name, test_logical_id=str(uuid4()))
    assert test_1.refresh().test_index == 1

    test_2 = started_session.report_test_start(name=test_name, test_logical_id=str(uuid4()))
    assert test_2.refresh().test_index == 2


def test_test_index_custom(started_session, test_name):
    test_1 = started_session.report_test_start(name=test_name, test_index=600)
    assert test_1.refresh().test_index == 600


def test_report_interrupted(started_test):
    started_test.report_interrupted()
    assert started_test.refresh().status.lower() == 'interrupted'


def test_interruptions_after_test_end(started_test):
    started_test.report_end()
    started_test.report_interrupted()
    assert started_test.refresh().status.lower() == 'interrupted'


def test_test_parameters(started_session, test_name, params):
    test = started_session.report_test_start(
        name=test_name, parameters=params)
    expected = params.copy()
    if 'obj_param' in expected:
        expected['obj_param'] = str(expected['obj_param'])
    test.refresh()
    got_params = test.parameters
    assert expected['very_long_param'] != got_params['very_long_param']
    assert expected['very_long_param'][:10] == got_params['very_long_param'][:10]
    expected.pop('very_long_param')
    got_params.pop('very_long_param')
    assert got_params == expected


def test_append_upcoming_with_ended_session(ended_session, test_name, file_name, class_name):
    test_list = [{'test_logical_id': str(uuid4()),
                  'file_name': file_name,
                  'name': test_name,
                  'class_name': class_name
                 }]
    with raises_conflict():
        ended_session.report_upcoming_tests(tests=test_list)


def test_append_upcoming_report_all_tests(started_session, test_name, file_name, class_name):
    test_logical_id = str(uuid4())
    test1 = {'test_logical_id': test_logical_id,
             'name': test_name,
             'file_name': file_name,
             'class_name': class_name
            }
    test2 = {'test_logical_id': str(uuid4()),
             'name': test_name,
             'file_name': file_name,
             'class_name': class_name
            }
    test_list = [test1, test2]
    all_tests = started_session.query_tests(include_planned=True).all()
    assert len(all_tests) == 0

    started_session.report_upcoming_tests(tests=test_list)
    all_tests = started_session.query_tests(include_planned=True).all()
    assert len(all_tests) == 2

    started_session.report_test_start(name=test_name, test_logical_id=test_logical_id)
    all_tests = started_session.query_tests(include_planned=True).all()
    assert len(all_tests) == 2

    started_session.report_test_start(name=test_name, test_logical_id=str(uuid4()))
    all_tests = started_session.query_tests(include_planned=True).all()
    assert len(all_tests) == 3


def test_cannot_report_interruption_on_planned_test(started_session, test_name, file_name, class_name):
    test_logical_id = str(uuid4())
    test1 = {'test_logical_id': test_logical_id,
             'name': test_name,
             'file_name': file_name,
             'class_name': class_name
            }
    test_list = [test1]
    started_session.report_upcoming_tests(tests=test_list)
    test = started_session.query_tests(include_planned=True)[0]
    with raises_conflict():
        test.report_interrupted()
    assert test.refresh().status.lower() != 'interrupted'


def test_skipped_test_adds_error(started_session, started_test):
    started_test.mark_skipped("skipped")
    started_test.add_error("error")
    started_test.report_end()
    started_session.report_end()
    assert started_session.refresh().num_skipped_tests == 0
    assert started_session.num_error_tests == 1
    assert started_session.num_finished_tests == 1


def test_errored_test_adds_skip(started_session, started_test):
    started_test.add_error("error")
    started_test.mark_skipped("skipped")
    started_test.report_end()
    started_session.report_end()
    assert started_session.refresh().num_skipped_tests == 0
    assert started_session.num_error_tests == 1
    assert started_session.num_finished_tests == 1


def test_ended_error_test_adds_skip(started_session, started_test):
    started_test.add_error("error")
    started_test.report_end()
    started_test.mark_skipped("skipped")
    started_session.report_end()
    started_session.refresh()
    assert started_session.num_skipped_tests == 0
    assert started_session.num_error_tests == 1
    assert started_session.num_finished_tests == 1


def test_error_failure_test_adds_skip(started_session, started_test):
    started_test.add_error("error", is_failure=True)
    started_test.add_error("error", is_failure=False)
    started_test.mark_skipped("skipped")
    started_test.report_end()
    started_session.report_end()
    started_session.refresh()
    assert started_session.num_skipped_tests == 0
    assert started_session.num_error_tests == 1
    assert started_session.num_failed_tests == 0



@pytest.fixture(params=[True, False])
def params(request):
    encodable = request.param

    returned = {
        'int_param': 2,
        'str_param': 'some string',
        'very_long_param': 'very long' * 1000,
        'float_param': 1.5,
        'bool_param': True,
        'null_param': None,
    }

    if not encodable:
        returned['obj_param'] = object()

    return returned
