import requests

import flux

from .utils import raises_not_found


def test_add_error(error_container, error_data, webapp):
    timestamp = flux.current_timeline.time()
    error_container.add_error(error_data['exception'],
                              error_data['exception_type'],
                              error_data['traceback'],
                              timestamp=timestamp)
    error_container.refresh()
    [first_error] = error_container.query_errors()
    assert first_error.message == error_data['exception']
    assert first_error.exception_type == error_data['exception_type']
    assert first_error.timestamp == timestamp
    assert first_error.traceback is None
    resp = requests.get(webapp.url.add_path(first_error.traceback_url))
    resp.raise_for_status()
    assert resp.json() == error_data['traceback']


def test_add_error_just_msg(error_container):
    error_container.add_error('msg')
    [err] = error_container.refresh().query_errors()
    assert err.message == 'msg'
    assert not err.is_failure


def test_add_failure_just_msg(error_container):
    error_container.add_failure('msg')
    [err] = error_container.refresh().query_errors()
    assert err.message == 'msg'
    assert err.is_failure

def test_add_failure_num_failures(error_container):
    error_container.add_failure('F')
    error_container.report_end()
    assert error_container.refresh().num_failures == 1
    assert error_container.refresh().num_errors == 0

def test_add_failure_status(error_container):
    error_container.add_failure('F')
    error_container.report_end()
    assert error_container.refresh().status == 'FAILURE'


def test_add_error_num_errors(error_container):
    error_container.add_error('E')
    error_container.report_end()
    assert error_container.refresh().num_failures == 0
    assert error_container.refresh().num_errors == 1

def test_add_error_status(error_container):
    error_container.add_error('E')
    error_container.report_end()
    assert error_container.refresh().status == 'ERROR'



def test_add_error_no_timestamp(error_container, error_data, webapp):
    error_container.add_error(error_data['exception'],
                           error_data['exception_type'],
                           error_data['traceback'])
    error_container.refresh()
    [first_error] = error_container.query_errors()
    assert first_error.message == error_data['exception']
    assert first_error.exception_type == error_data['exception_type']
    assert first_error.timestamp == flux.current_timeline.time()
    assert requests.get(webapp.url.add_path(first_error.traceback_url)).json() == error_data['traceback']


def test_add_error_nonexistent(nonexistent_error_container, error_data):
    with raises_not_found():
        nonexistent_error_container.add_error(error_data['exception'],
                                              error_data['exception_type'],
                                              error_data['traceback'])
