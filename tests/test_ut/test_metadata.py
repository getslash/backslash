import pytest

from .utils import raises_bad_request, raises_conflict, raises_not_found


def test_add_metadata(metadata_holder, metadata_key, metadata_value):
    metadata_holder.set_metadata(metadata_key, metadata_value)
    another_key = 'another_key'
    another_value = {'another': 31337}
    metadata_holder.set_metadata(another_key, another_value)
    assert metadata_holder.get_metadata() == {
        metadata_key: metadata_value,
        another_key: another_value
    }


def test_add_metadata_nonexistent_session(nonexistent_session):
    with raises_not_found():
        nonexistent_session.set_metadata('foo', 'bar')
