import logbook
import os
import queue
from yarl import URL
import requests
import threading
import time
from flask import has_request_context, request
from sqlalchemy import event
from sqlalchemy.engine import Engine

_TOTAL_HEADER_NAME = "X-Timing-Total"
_ACTIVE_HEADER_NAME = "X-Timing-Active"
_DB_HEADER_NAME = "X-Timing-DB"
_API_ENDPOINT_HEADER_NAME = "X-API-Endpoint"

_backend_name = 'python-backend-generic'

def set_backend_name(new_name):
    global _backend_name
    if new_name is not None:
        _backend_name = new_name

_logger = logbook.Logger(__name__)


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    if not has_request_context():
        return
    profile_data = request.profile_data
    profile_data[_DB_HEADER_NAME] -= time.perf_counter()


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    if not has_request_context():
        return
    profile_data = request.profile_data
    profile_data[_DB_HEADER_NAME] += time.perf_counter()


def profile_request_start():
    request.profile_data = {
        _TOTAL_HEADER_NAME: -time.perf_counter(),
        _ACTIVE_HEADER_NAME: -time.process_time(),
        _DB_HEADER_NAME: 0,
    }


def profile_request_end(response):
    profile_data = request.profile_data
    profile_data[_TOTAL_HEADER_NAME] += time.perf_counter()
    profile_data[_ACTIVE_HEADER_NAME] += time.process_time()
    endpoint = profile_data[
        _API_ENDPOINT_HEADER_NAME
    ] = f"{request.endpoint}:{request.method}"
    total = profile_data[_TOTAL_HEADER_NAME]
    active = profile_data[_ACTIVE_HEADER_NAME]
    db = profile_data[_DB_HEADER_NAME]

    _send_metrics(db=db, active=active, total=total, endpoint=endpoint)

    response.headers.extend(profile_data)
    response.headers['X-Backslash-Backend'] = _backend_name
    return response


_REQUEST_METRICS_URL = _SESSION_START_METRICS_URL = _TEST_START_METRICS_URL = None
_METRICS_SERVER_URL = os.environ.get("METRICS_URL")
if _METRICS_SERVER_URL is not None:
    _REQUEST_METRICS_URL = str(URL(_METRICS_SERVER_URL) / "metrics" / "request")
    _SESSION_START_METRICS_URL = str(
        URL(_METRICS_SERVER_URL) / "metrics" / "session_start"
    )
    _TEST_START_METRICS_URL = str(URL(_METRICS_SERVER_URL) / "metrics" / "test_start")


def _send_metrics(**fields):
    _safe_http_post(_REQUEST_METRICS_URL, params=fields, timeout=1)


def notify_session_start():
    _safe_http_post(_SESSION_START_METRICS_URL, timeout=1)


def notify_test_start():
    _safe_http_post(_TEST_START_METRICS_URL, timeout=1)


def _safe_http_post(url, *args, **kwargs):
    if url is not None:
        try:
            resp = requests.post(url, *args, **kwargs)
        except Exception:
            _logger.error(
                f"Swallowing exception during metrics reporting to {url}", exc_info=True
            )
