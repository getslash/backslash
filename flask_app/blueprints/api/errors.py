import gzip
import json
import os
from io import TextIOWrapper
from uuid import uuid4

import requests

from flask import current_app, request
from flask_simple_api import error_abort
from sqlalchemy.orm.exc import NoResultFound
from urlobject import URLObject as URL

from ...models import Error, Session, Test, db
from ...utils import get_current_time, statuses
from .blueprint import API

NoneType = type(None)


@API(version=2)
def add_error(message: str, exception_type: (str, NoneType)=None, traceback: (list, NoneType)=None, timestamp: (float, int)=None, test_id: int=None, session_id: int=None, is_failure: bool=False):
    # pylint: disable=superfluous-parens
    if not ((test_id is not None) ^ (session_id is not None)):
        error_abort('Either test_id or session_id required')

    if timestamp is None:
        timestamp = get_current_time()
    if test_id is not None:
        cls = Test
        object_id = test_id
    else:
        cls = Session
        object_id = session_id

    try:
        obj = cls.query.filter(cls.id == object_id).one()
        increment_field = cls.num_failures if is_failure else cls.num_errors
        cls.query.filter(cls.id == object_id).update(
            {increment_field: increment_field + 1})
        obj.errors.append(Error(message=message,
                                exception_type=exception_type,
                                traceback_url=_normalize_traceback_get_url(traceback),
                                is_failure=is_failure,
                                timestamp=timestamp))
        if obj.end_time is not None:
            if cls is Test:
                if is_failure and obj.status not in (statuses.FAILURE, statuses.ERROR):
                    obj.status = statuses.FAILURE
                    obj.session.num_failed_tests = Session.num_failed_tests + 1
                elif not is_failure and obj.status != statuses.ERROR:
                    if obj.status == statuses.FAILURE:
                        db.session.num_failed_tests = Session.num_failed_tests - 1
                    obj.status = statuses.ERROR
                    obj.session.num_error_tests = Session.num_error_tests + 1
        db.session.add(obj)

    except NoResultFound:
        error_abort('Entity not found', code=requests.codes.not_found)
    db.session.commit()


def _normalize_traceback_get_url(traceback_json):
    if traceback_json:
        for frame in traceback_json:
            code_string = frame['code_string']
            if code_string:
                code_string = code_string.splitlines()[-1]
            frame['code_string'] = code_string
    url, location = _get_new_traceback_save_location()
    _ensure_dir(os.path.dirname(location))
    with open(location, 'wb') as raw_file:
        with gzip.GzipFile(fileobj=raw_file, mode='wb') as gzip_file:
            with TextIOWrapper(gzip_file) as f:
                json.dump(traceback_json, f)


    return url

def _get_new_traceback_save_location():
    uuid = str(uuid4()).replace('-', '')
    prefix = uuid[:2]
    location = os.path.join(current_app.config['TRACEBACK_DIR'], prefix, uuid)
    location += '.gz'
    url = '/rest/tracebacks/{}'.format(uuid)
    return url, location

def _ensure_dir(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)
