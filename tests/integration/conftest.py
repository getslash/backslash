import time
import subprocess

import requests
import pytest
from urlobject import URLObject

_docker_running = False

@pytest.fixture(autouse=True, scope='session')
def cleanup_docker(request):
    @request.addfinalizer
    def cleanup():
        if _docker_running:
            _stop_docker()


@pytest.fixture
def integration_url(request, capsys, timeout=30):
    start_docker = request.config.getoption('--start-docker')
    url = request.config.getoption("--app-url")

    if start_docker:
        _start_docker(capsys)
        if url is None:
            url = 'http://127.0.0.1:8000'

    if url is None:
        pytest.skip('No integration URL provided')


    end_time = time.time() + timeout
    retry = 0
    while time.time() < end_time:
        retry += 1

        if retry > 0:
            time.sleep(3)

        try:
            resp = requests.get(url)
        except requests.RequestException:
            continue

        if resp.ok:
            return URLObject(url)

    raise RuntimeError(f'URl {url} did not become available in time')


def _start_docker(capsys):
    global _docker_running
    if _docker_running:
        return
    _docker_running = True
    with capsys.disabled():
        _run_docker_compose('build')
        _run_docker_compose('up -d')
        _docker_running = True

def _stop_docker():
    global _docker_running
    _run_docker_compose('down')
    _docker_running = False

def _run_docker_compose(cmd):
    subprocess.run(
        f'docker-compose -f docker/docker-compose.yml -f docker/docker-compose-testing-override.yml -p backslash-testing {cmd}',
        shell=True,
        check=True,
    )
