import copy
import pytest

@pytest.mark.parametrize('code', [200, 400, 503])
def test_codes(code, proxy):
    assert proxy.get(f'/code/{code}').status_code == code


@pytest.mark.parametrize('method', ['post', 'put'])
def test_json_request(proxy, method):
    expected = {'some': 'json', 'with': {'nested': 'data', 'and_numbers': 2, 'and_lists': []}}
    resp = proxy.request(method, '/json_echo', json=copy.deepcopy(expected))
    resp.raise_for_status()
    assert resp.json() == {
        'method': method,
        'json': expected,
    }
