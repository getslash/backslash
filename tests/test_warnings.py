import pytest

from .utils import raises_not_found
from backslash.test import Test as TestType


def test_add_warnings(warning_container, filename, lineno, message, timestamp):
    w = warning_container.add_warning(
        filename=filename, lineno=lineno, message=message, timestamp=timestamp)
    assert warning_container.refresh().num_warnings == 1
    [fetched] = warning_container.query_warnings()
    assert fetched.message == message
    assert fetched.lineno == lineno
    assert fetched.timestamp == timestamp
    assert fetched.filename == filename
    if isinstance(warning_container, TestType):
        assert warning_container.get_session().num_warnings == 1

def test_add_warnings_nonexistent_session(warning_container, message):
    warning_container.id *= 1000
    with raises_not_found():
        warning_container.add_warning(message=message)


@pytest.fixture
def filename():
    return 'some_filename.py'


@pytest.fixture
def timestamp():
    return 198734.2


@pytest.fixture
def lineno():
    return 23


@pytest.fixture
def message():
    return 'This is a serious warning'
