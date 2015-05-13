import click

import logbook

from flask_app import tasks
from flask_app.app import create_app
from .bootstrapping import requires_env

_logger = logbook.Logger(__name__)

@click.group()
def celery():
    pass


@celery.command()
@click.argument('name')
@requires_env('app')
def task(name):
    task = getattr(tasks, name, None)
    if task is None:
        click.abort('Could not find task named {}'.format(task))
    with create_app().app_context():
        task()
