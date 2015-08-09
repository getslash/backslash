from __future__ import absolute_import

from logging import Formatter
from logbook.compat import LoggingHandler
from logging.handlers import SysLogHandler
from celery import Celery
from celery.signals import after_setup_task_logger, after_setup_logger
import os


queue = Celery('tasks', broker='redis://localhost')
queue.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ENABLE_UTC=True,
)

def setup_log(**args):
    if os.path.exists("/dev/log"):
        hl = SysLogHandler('/dev/log')
        hl.setLevel(args['loglevel'])
        formatter = Formatter("%(message)s")
        hl.setFormatter(formatter)
        args['logger'].addHandler(hl)

    LoggingHandler().push_application()


after_setup_logger.connect(setup_log)
after_setup_task_logger.connect(setup_log)
