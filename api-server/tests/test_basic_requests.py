import pytest

@pytest.mark.parametrize('code', [200, 400, 503])
def test_codes(code, proxy):
    assert proxy.get(f'/code/{code}').status_code == code

def test_upload_nonstreaming(proxy, random_data):
    assert proxy.post('/do_checksum', data=random_data.data).json()['sha1'] == random_data.sha1

def test_upload_streaming(proxy, random_stream):
    resp = proxy.post('/do_checksum', data=random_stream.stream)
    resp.raise_for_status()
    random_stream.wait()
    assert resp.json()['sha1'] == random_stream.digest

def test_upload_streaming_gzip(proxy, random_gzip):
    resp = proxy.post('/do_checksum', data=random_gzip.data, headers={'Content-encoding': 'gzip'})
    resp.raise_for_status()
    assert resp.json()['sha1'] != random_gzip.outer_digest
    assert resp.json()['sha1'] == random_gzip.inner_digest
