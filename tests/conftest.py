import pytest
from urlobject import URLObject as URL

def pytest_addoption(parser):
    parser.addoption("--www-port", action="store", default=8080, type=int)

@pytest.fixture
def webapp_url(request):
    port = request.config.getoption("--www-port")
    return URL("http://127.0.0.1").with_port(port)
