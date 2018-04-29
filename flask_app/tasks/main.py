from __future__ import absolute_import

import functools
import os
import sys

import logbook

from celery import Celery
from celery.signals import after_setup_logger, after_setup_task_logger

from ..app import create_app


_logger = logbook.Logger(__name__)


queue = Celery('tasks', broker=os.environ.get('BACKSLASH_CELERY_BROKER_URL',
                                              'amqp://guest:guest@localhost'))
queue.conf.update(
    CELERY_ENABLE_UTC=True,
    CELERYBEAT_SCHEDULE={
        'delete_discarded_sessions': {
            'task': 'flask_app.tasks.maintenance.delete_discarded_sessions',
            'schedule': 24 * 60 * 60,
        },
    },
)

def setup_log(**_):
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

from . import replications # pylint: disable=unused-import
from . import maintenance  # pylint: disable=unused-import
from . import migrations   # pylint: disable=unused-import
################################################################################

