import pytest

@pytest.mark.parametrize('code', [200, 400, 503])
def test_codes(code, proxy):
    assert proxy.get(f'/code/{code}').status_code == code
