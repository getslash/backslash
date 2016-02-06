import os
from multiprocessing import cpu_count

import click

from .bootstrapping import from_env_bin, requires_env, from_project_root
from .params import APP_NAME

_UNIX_SOCKET_NAME = "/var/run/{}/wsgi.sock".format(APP_NAME)


@click.command()
@requires_env("app")
def run_gunicorn():
    num_workers = (2 * cpu_count()) + 1
    gunicorn_bin = from_env_bin('gunicorn')
    cmd = [gunicorn_bin, '--log-syslog', '-b', 'unix://{}'.format(_UNIX_SOCKET_NAME), 'flask_app.wsgi:app', '--chdir', from_project_root('.'), '-w', str(num_workers)]
    os.execv(gunicorn_bin, cmd)

