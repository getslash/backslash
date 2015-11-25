import requests

from .utils import raises_not_found


def test_add_metadata(metadata_holder, metadata_key, metadata_value):
    metadata_holder.set_metadata(metadata_key, metadata_value)
    another_key = 'another_key'
    another_value = {'another': 31337}
    metadata_holder.set_metadata(another_key, another_value)
    assert metadata_holder.get_metadata() == {
        metadata_key: metadata_value,
        another_key: another_value
    }


def test_add_metadata_dict(metadata_holder, metadata_key, metadata_value):
    another_key = 'another_key'
    another_value = {'another': 31337}

    metadata_holder.set_metadata_dict({metadata_key: metadata_value, another_key: another_value})
    assert metadata_holder.get_metadata() == {
        metadata_key: metadata_value,
        another_key: another_value
    }



def test_get_metadata_by_logical_id(metadata_holder, metadata_key, metadata_value, client):
    assert metadata_holder.logical_id
    metadata_holder.set_metadata(metadata_key, metadata_value)
    result = client.api.call_function(
        'get_metadata', {
            'entity_type': metadata_holder.type,
            'entity_id': metadata_holder.logical_id,
            })
    assert result == {metadata_key: metadata_value}



def test_create_session_with_metadata(client, metadata):
    session = client.report_session_start(metadata=metadata)
    assert session.get_metadata() == metadata


def test_add_metadata_nonexistent_session(nonexistent_session):
    with raises_not_found():
        nonexistent_session.set_metadata('foo', 'bar')
