import errno
import flux
from flask import current_app
import functools
import itertools
import logbook
import os
from .main import queue, needs_app_context
from .. import models
from ..utils.redis import get_redis_client


_logger = logbook.Logger(__name__)

_RELIABLE_TASKS = []


def reliable_task(task_func, stale_timeout=10 * 60):
    assert not hasattr(task_func, 'delay'), 'reliable_task decorator must be applied before the celery.task'
    task_key = f'reliable_{task_func.__module__}_{task_func.__name__}'

    @functools.wraps(task_func)
    def new_func(*args, **kwargs):
        get_redis_client().setex(task_key, 'true', time=stale_timeout)
        return task_func(*args, **kwargs)

    returned = queue.task(new_func)
    _RELIABLE_TASKS.append((returned, task_key))
    return returned

@queue.task
def rerun_stale_tasks():
    client = get_redis_client()
    for task_func, key in _RELIABLE_TASKS:
        if client.get(key) is None:
            _logger.debug('Rerunning stale task {}...', task_func)
            task_func.delay()


@queue.task
@needs_app_context
def delete_discarded_sessions(ignore_date=False):
    query = models.Session.query
    if ignore_date:
        query = query.filter(models.Session.delete_at != None)
    else:
        query = query.filter(models.Session.delete_at <= flux.current_timeline.time())
    while True:
        session = query.first()
        if not session:
            return
        tests = models.Test.query.filter(models.Test.session_id == session.id)
        for error in itertools.chain(session.errors, (error for t in tests for error in t.errors)):
            if not error.traceback_url:
                continue
            traceback_uuid = error.traceback_url.rsplit('/', 1)[-1]
            traceback_filename = os.path.join(
                current_app.config['TRACEBACK_DIR'], traceback_uuid[:2], traceback_uuid + '.gz')
            _logger.debug('Deleting error {.id} ({})', error, traceback_filename)
            try:
                os.unlink(traceback_filename)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise
        _logger.debug('Deleting session {0.id} (Logical id {0.logical_id})', session)
        models.db.session.execute('DELETE FROM SESSION WHERE id = :id', {'id': session.id})
        models.db.session.commit()
