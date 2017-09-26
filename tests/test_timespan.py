import datetime
import flux
import pendulum


_MIN_THRESHOLD = datetime.timedelta(seconds=0.01)

def test_timespan(session_or_test, get_real_object):
    obj = session_or_test

    timespan = get_real_object(obj).timespan
    assert timespan is not None
    span_start = timespan.lower
    assert span_start is not None
    assert timespan.upper is None

    assert abs(timespan.lower - pendulum.fromtimestamp(obj.start_time).astimezone()) < _MIN_THRESHOLD

    duration = 10

    flux.current_timeline.sleep(duration) # pylint: disable=no-member

    obj.report_end()
    timespan = get_real_object(obj).timespan
    assert timespan is not None
    assert timespan.upper is not None
    assert timespan.lower == span_start

    assert abs((timespan.upper - timespan.lower) - datetime.timedelta(seconds=duration)) < _MIN_THRESHOLD


def test_timespan_keepalive(started_session, get_real_object):
    obj = started_session

    assert obj.keepalive_interval
    assert get_real_object(obj).timespan.upper is None

    obj.send_keepalive()

    timespan = get_real_object(obj).timespan
    assert timespan.upper is not None
    assert abs(timespan.upper - timespan.lower - datetime.timedelta(seconds=obj.keepalive_interval)) < _MIN_THRESHOLD


def test_timespan_started_test(started_test, get_real_object):
    assert get_real_object(started_test).timespan.upper is not None


def test_timespan_started_test_session_keepalive(started_session, started_test, get_real_object):
    test_obj = get_real_object(started_test)
    original_end = test_obj.timespan.upper
    original_start = test_obj.timespan.lower
    flux.current_timeline.sleep(10)
    started_session.send_keepalive()
    test_obj = get_real_object(started_test)
    assert test_obj.timespan.lower == original_start
    assert test_obj.timespan.upper > original_end
    assert test_obj.timespan.upper == get_real_object(started_session).timespan.upper
