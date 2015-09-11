from __future__ import absolute_import

import functools
import os
import sys

import logbook

from celery import Celery
from celery.signals import after_setup_logger, after_setup_task_logger

from .app import create_app

_logger = logbook.Logger(__name__)


queue = Celery('tasks', broker='redis://localhost')
queue.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ENABLE_UTC=True,
)

def setup_log(**args):
    logbook.SyslogHandler().push_application()
    logbook.StreamHandler(sys.stderr, bubble=True).push_application()

APP = None

def needs_app_context(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        global APP

        if APP is None:
            APP = create_app()

        with APP.app_context():
            return f(*args, **kwargs)

    return wrapper


after_setup_logger.connect(setup_log)
after_setup_task_logger.connect(setup_log)
