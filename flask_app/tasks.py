from __future__ import absolute_import

from celery import Celery

queue = Celery('tasks', broker='redis://localhost')
queue.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ENABLE_UTC=True,
)
