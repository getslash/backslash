from contextlib import ExitStack, contextmanager
import gzip
import json
import os
from io import TextIOWrapper
import shutil
from uuid import uuid4

import requests

from flask import current_app, request, jsonify
from flask_simple_api import error_abort
from sqlalchemy.orm.exc import NoResultFound

from ...models import Error, Session, Test, db
from ...utils import get_current_time, statuses
from .blueprint import API
from ..rest import blueprint as rest_blueprint

NoneType = type(None)


@API(version=4)
def add_error(message: str, exception_type: (str, NoneType)=None, traceback: (list, NoneType)=None, timestamp: (float, int)=None, test_id: int=None, session_id: int=None, is_failure: bool=False, is_interruption: bool=False): # pylint: disable=bad-whitespace
    # pylint: disable=superfluous-parens
    if not ((test_id is not None) ^ (session_id is not None)):
        error_abort('Either test_id or session_id required')

    if is_failure and is_interruption:
        error_abort('Interruptions cannot be marked as failures')

    if timestamp is None:
        timestamp = get_current_time()
    if test_id is not None:
        cls = Test
        object_id = test_id
    else:
        cls = Session
        object_id = session_id

    message = message.replace("\x00", "\\x00")
    try:
        obj = cls.query.filter(cls.id == object_id).one()
        if is_failure:
            increment_field = cls.num_failures
        elif is_interruption:
            increment_field = cls.num_interruptions
        else:
            increment_field = cls.num_errors
        cls.query.filter(cls.id == object_id).update(
            {increment_field: increment_field + 1})
        err = Error(message=message,
                    exception_type=exception_type,
                    traceback_url=_normalize_traceback_get_url(traceback),
                    is_interruption=is_interruption,
                    is_failure=is_failure,
                    timestamp=timestamp)
        obj.errors.append(err)
        if not is_interruption and obj.end_time is not None:
            if cls is Test:
                if is_failure and obj.status not in (statuses.FAILURE, statuses.ERROR):
                    obj.status = statuses.FAILURE
                    obj.session.num_failed_tests = Session.num_failed_tests + 1
                elif not is_failure and obj.status != statuses.ERROR:
                    if obj.status == statuses.FAILURE:
                        obj.session.num_failed_tests = Session.num_failed_tests - 1
                        if obj.session.parent:
                            obj.session.parent.num_failed_tests = obj.session.parent.num_failed_tests + 1
                    obj.status = statuses.ERROR
                    obj.session.num_error_tests = Session.num_error_tests + 1
                    if obj.session.parent:
                        obj.session.parent.num_error_tests = obj.session.parent.num_error_tests + 1
        if cls is Session and obj.parent is not None:
            if is_failure:
                obj.parent.num_failures = obj.parent.num_failures + 1
            else:
                obj.parent.num_errors = obj.parent.num_errors + 1
        db.session.add(obj)

    except NoResultFound:
        error_abort('Entity not found', code=requests.codes.not_found)
    db.session.commit()
    return err


@rest_blueprint.route('/errors/<int:error_id>/traceback', methods=['PUT'])
def upload_traceback(error_id):
    error = Error.query.get_or_404(error_id)
    if error.traceback_url is not None:
        error_abort('Error already has an associated traceback', requests.codes.conflict)
    temporary_location = os.path.join(current_app.config['TRACEBACK_DIR'], 'incomplete', str(error.id))
    _ensure_dir(os.path.dirname(temporary_location))
    try:
        with _compressed_output(request.stream, temporary_location) as outfile:
            shutil.copyfileobj(request.stream, outfile)
        url, location = _get_new_traceback_save_location()
        _ensure_dir(os.path.dirname(location))
        os.rename(temporary_location, location)
        error.traceback_url = url
    except Exception:           # pylint: disable=broad-except
        if os.path.exists(temporary_location):
            os.unlink(temporary_location)
        raise
    error.traceback_size = os.stat(location).st_size
    db.session.add(error)
    db.session.commit()
    return jsonify({'traceback_url': error.traceback_url})


@contextmanager
def _compressed_output(input_stream, output_path):
    header = input_stream.read(3)
    with ExitStack() as stack:
        f = stack.enter_context(open(output_path, 'wb'))
        if header != b'\x1f\x8b\x08':
            # not compressed already
            f = stack.enter_context(gzip.GzipFile(fileobj=f))

        f.write(header)
        yield f



def _normalize_traceback_get_url(traceback_json):
    if traceback_json is None:
        return None

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
