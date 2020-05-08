import json
import time
import subprocess

import requests
import pytest
from urlobject import URLObject

_docker_running = False


def pytest_addoption(parser):
    parser.addoption(
        "--app-url", action="store", default=None, help="Integration App URL"
    )
    parser.addoption("--admin-username", action="store", default="admin@localhost")
    parser.addoption("--admin-password", action="store", default="12345678")


@pytest.fixture(autouse=True, scope="session")
def cleanup_docker(request):
    @request.addfinalizer
    def cleanup():
        if _docker_running:
            _stop_docker()


@pytest.fixture(scope="session")
def integration_url(request, timeout=30):
    url = request.config.getoption("--app-url")

    if url is None:
        raise RuntimeError("No integration URL provided")

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
            returned = URLObject(url)
            _do_setup_if_needed(returned)
            return returned

    raise RuntimeError(f"URl {url} did not become available in time")


def _do_setup_if_needed(url):
    with requests.Session() as s:
        s.headers.update({"Content-type": "application/json"})
        resp = s.post(url.add_path("api/get_app_config"), data="{}")
        resp.raise_for_status()
        if resp.json()["result"]["setup_needed"]:
            resp = s.post(
                url.add_path("api/setup"),
                data=json.dumps(
                    {
                        "config": {
                            "admin_user_email": "admin@localhost",
                            "admin_user_password": "12345678",
                        }
                    }
                ),
            )
            resp.raise_for_status()


def _start_docker():
    global _docker_running
    if _docker_running:
        return
    _docker_running = True
    _run_docker_compose("build")
    _run_docker_compose("up -d")
    _docker_running = True


def _stop_docker():
    global _docker_running
    _run_docker_compose("down")
    _docker_running = False


def _run_docker_compose(cmd):
    subprocess.run(
        f"docker-compose -f docker/docker-compose.yml -f docker/docker-compose-testing-override.yml -p backslash-testing {cmd}",
        shell=True,
        check=True,
    )
