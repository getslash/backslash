import functools
import socket
from contextlib import closing

import logbook
import requests
from waiting import wait


def _is_http_responsive():
    try:
        logbook.debug("Trying to connect to HTTP server...")
        resp = requests.get("http://127.0.0.1/")
        resp.raise_for_status()
    except Exception:
        logbook.error("HTTP not available yet", exc_info=True)
        return False
    return True

def wait_for_travis_availability():

    _wait = functools.partial(wait, timeout_seconds=300, sleep_seconds=5)

    logbook.info("Waiting for travis installation to settle down...")
    _wait(_is_http_responsive, waiting_for="HTTP Service to become available")
    logbook.info("Success: travis install complete")

if __name__ == "__main__":
    wait_for_travis_availability()
