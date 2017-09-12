from __future__ import absolute_import

from datetime import timedelta
import errno
import itertools
import functools
import os
import sys

from flask import current_app
import logging
import logging.handlers
import logbook

from celery import Celery
from celery.signals import after_setup_logger, after_setup_task_logger
import flux

from .app import create_app
from . import models
from .utils import get_current_time

_logger = logbook.Logger(__name__)


queue = Celery('tasks', broker=os.environ.get('BACKSLASH_CELERY_BROKER_URL', 'amqp://guest:guest@localhost'))
queue.conf.update(
    CELERY_ENABLE_UTC=True,
    CELERYBEAT_SCHEDULE={
        'start-live-migrations': {
            'task': 'flask_app.tasks.start_live_migrations',
            'schedule': 300,
        },
        'delete_discarded_sessions': {
            'task': 'flask_app.tasks.delete_discarded_sessions',
            'schedule': 24 * 60 * 60,
        },
    },
)

def setup_log(**args):
    logbook.StreamHandler(sys.stderr).push_application()

APP = None

def needs_app_context(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        global APP              # pylint: disable=global-statement

        if APP is None:
            APP = create_app(setup_logging=False)

        with APP.app_context():
            return f(*args, **kwargs)

    return wrapper


after_setup_logger.connect(setup_log)
after_setup_task_logger.connect(setup_log)
################################################################################


@queue.task
@needs_app_context
def start_live_migrations():
    pending = models.BackgroundMigration.query.filter_by(started=False).all()
    started = models.BackgroundMigration.query.filter_by(started=True, finished=False).all()
    if pending and not started:
        do_live_migrate.delay()


@queue.task
@needs_app_context
def do_live_migrate():
    for migration in models.BackgroundMigration.query\
                                             .filter_by(finished=False)\
                                             .order_by(models.BackgroundMigration.id.asc()).all():
        if not migration.started:
            migration.started = True
            migration.started_time = get_current_time()
            num_rows = models.db.session.execute(migration.remaining_num_items_query).scalar()
            migration.remaining_num_objects = num_rows
            migration.total_num_objects = num_rows
            models.db.session.commit()

        num_objects = migration.remaining_num_objects

        _logger.debug('Running migration: {.name}...', migration)

        while True:
            result = models.db.session.execute(migration.update_query, {'batch_size': migration.batch_size})
            if result.rowcount == 0:
                migration.remaining_num_objects = 0
                migration.finished = True
                migration.finished_time = get_current_time()
            else:
                num_objects = max(0, num_objects - result.rowcount)
                migration.remaining_num_objects = num_objects

            models.db.session.commit()
            if result.rowcount == 0:
                break

@queue.task
@needs_app_context
def delete_discarded_sessions(ignore_date=False):
    query = models.Session.query
    if ignore_date:
        query = query.filter(models.Session.delete_at != None)
    else:
        query = query.filter(models.Session.delete_at <= flux.current_timeline.time())
    sessions = query.all()
    for session in sessions:
        tests = models.Test.query.filter(models.Test.session_id == session.id)
        for error in itertools.chain(session.errors, (error for t in tests for error in t.errors)):
            if not error.traceback_url:
                continue
            traceback_uuid = error.traceback_url.rsplit('/', 1)[-1]
            traceback_filename = os.path.join(current_app.config['TRACEBACK_DIR'], traceback_uuid[:2], traceback_uuid + '.gz')
            _logger.debug('Deleting error {.id} ({})', error, traceback_filename)
            try:
                os.unlink(traceback_filename)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise
        _logger.debug('Deleting session {0.id} (Logical id {0.logical_id})', session)
        models.db.session.execute('DELETE FROM SESSION WHERE id = :id', {'id': session.id})
        models.db.session.commit()
