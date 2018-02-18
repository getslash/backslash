# pylint: disable=missing-docstring, redefined-outer-name
import flux
import pytest
from .utils import raises_conflict


def test_timing_start_end(timing_container, timing_action):
    assert timing_container.get_timings() == {}
    start_time = flux.current_timeline.time()
    timing_container.report_timing_start(timing_action)
    _validate_timing_ongoing(timing_container, timing_action)
    timing_container.report_timing_end(timing_action)
    total_time = flux.current_timeline.time() - start_time
    assert timing_container.get_timings()[timing_action] == total_time


def test_timing_start_start_end(timing_container, timing_action):
    timing_container.report_timing_start(timing_action)
    with raises_conflict():
        timing_container.report_timing_start(timing_action)

def test_timing_start_end_start_end(timing_container, timing_action):
    timing_container.report_timing_start(timing_action)
    flux.current_timeline.sleep(1)
    timing_container.report_timing_end(timing_action)
    flux.current_timeline.sleep(10)
    timing_container.report_timing_start(timing_action)
    flux.current_timeline.sleep(1)
    timing_container.report_timing_end(timing_action)
    assert timing_container.get_timings()[timing_action] == 2


def _validate_timing_ongoing(timing_container, timing_action):
    prev = None
    for _ in range(3):
        timings = timing_container.get_timings()
        assert len(timings) == 1
        if prev is not None:
            assert  0 < prev < timings[timing_action]
        else:
            prev = timings[timing_action]
            assert prev > 0
        flux.current_timeline.sleep(1)

@pytest.fixture
def timing_action():
    return 'waiting for something'
