import slash
import time

import warnings


def test_1():
    test = slash.plugins.manager.get_plugin('backslash').current_test
    test.report_timing_start('test-level-timer')
    time.sleep(1)
    test.report_timing_end('test-level-timer')


@slash.tag('tag_without_value')
def test_2():
    for i in range(5):
        warnings.warn('This is a warning!')


@slash.tag('tag_with_value', 'some_value')
def test_3():
    slash.skip_test('skipped')


@slash.parametrize('param1', ['string', {'some': 'dict'}])
def test_parametrized(param1, some_parameter):  # pylint: disable=unused-argument
    pass

def test_only_parametrized_fixture(some_parameter):
    pass


@slash.fixture
@slash.parametrize('param', ['very long' * 1000, 2, 'third arg'])
def some_parameter(param):
    return param


class SampleClassTest(slash.Test):

    def test_method(self):
        pass


@slash.parametrize('param', ['x.y', 'x(y'])
def test_4(param):  # pylint: disable=unused-argument
    pass


@slash.hooks.session_start.register
def emit_warning():
    slash.logger.warning('Session warning here')


@slash.hooks.session_start.register
def measure_something():
    session = slash.plugins.manager.get_plugin('backslash').session
    session.report_timing_start('session-level-timer')
    time.sleep(1)
    session.report_timing_end('session-level-timer')
