def test_client_header(proxy_method, header_name, header_value):
    resp = proxy_method("/headers", headers={header_name: header_value})
    resp.raise_for_status()
    assert resp.json()["headers"][header_name] == header_value


def test_server_header(proxy_method, header_name, header_value):
    resp = proxy_method(
        "/headers", params={header_name: header_value}
    )
    resp.raise_for_status()
    assert resp.headers[header_name] == header_value
