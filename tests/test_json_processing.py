from flask_app.utils.json import sanitize_json


def test_sanitize_json_none():
    assert sanitize_json(None) is None


def test_sanitize_json_long_values():
    value = sanitize_json({'x': 2, 'long': 'a' * 4096})
    assert value['x'] == 2
    assert value['long'].startswith('a')
    assert value['long'].endswith('a')
    assert len(value['long']) == 100
    assert '...' in value['long']
