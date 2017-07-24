import datetime
import flux


def test_timespan(session_or_test, get_real_object):
    obj = session_or_test

    timespan = get_real_object(obj).timespan
    assert timespan is not None
    span_start = timespan.lower
    assert span_start is not None
    assert timespan.upper is None

    threshold = datetime.timedelta(seconds=0.01)

    assert abs(timespan.lower - datetime.datetime.fromtimestamp(obj.start_time)) < threshold

    duration = 10

    flux.current_timeline.sleep(duration) # pylint: disable=no-member

    obj.report_end()
    timespan = get_real_object(obj).timespan
    assert timespan is not None
    assert timespan.upper is not None
    assert timespan.lower == span_start

    assert abs((timespan.upper - timespan.lower) - datetime.timedelta(seconds=duration)) < threshold


def test_timespan_keepalive(started_session, get_real_object):
    obj = started_session

    assert obj.keepalive_interval
    assert get_real_object(obj).timespan.upper is None

    obj.send_keepalive()

    timespan = get_real_object(obj).timespan
    assert timespan.upper is not None
    assert abs((timespan.upper - timespan.lower) - datetime.timedelta(seconds=obj.keepalive_interval)) < datetime.timedelta(seconds=0.01)
