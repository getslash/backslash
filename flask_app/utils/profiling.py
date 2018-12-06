import time
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import request, has_request_context


_TOTAL_HEADER_NAME = "X-Timing-Total"
_ACTIVE_HEADER_NAME = "X-Timing-Active"
_DB_HEADER_NAME = "X-Timing-DB"
_API_ENDPOINT_HEADER_NAME = "X-API-Endpoint"


import time
import logging

logging.basicConfig()
logger = logging.getLogger("myapp.sqltime")
logger.setLevel(logging.DEBUG)


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
    profile_data[_DB_HEADER_NAME] += 0
    profile_data[_API_ENDPOINT_HEADER_NAME] = f"{request.endpoint}:{request.method}"

    response.headers.extend(profile_data)
    return response
