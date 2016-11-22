from uuid import uuid4

import pytest


def test_add_label(client, label_container, label_name):
    for _ in range(3):
        kwargs = {'label': label_name}
        kwargs[label_container.type + '_id'] = label_container.id
        client.api.call.add_label(**kwargs)

        assert label_container.refresh().labels == [label_name]

def test_remove_label(client, label_container, label_name):
    kwargs = {'label': label_name}
    kwargs[label_container.type + '_id'] = label_container.id
    client.api.call.add_label(**kwargs)
    assert label_container.refresh().labels == [label_name]

    client.api.call.remove_label(**kwargs)
    assert label_container.refresh().labels == []



@pytest.fixture
def label_name():
    return str(uuid4())
