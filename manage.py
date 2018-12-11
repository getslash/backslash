#! /usr/bin/python
from __future__ import print_function
import os
import sys
import random
import string
import subprocess
from collections import defaultdict

from _lib.bootstrapping import from_project_root, from_env_bin

from _lib.params import APP_NAME
from _lib.frontend import frontend, ember
from _lib.db import db
from _lib.users import user
from _lib.celery import celery
from _lib.slash_running import suite
from _lib.utils import interact
import click
import logbook
import logbook.compat
import multiprocessing

##### ACTUAL CODE ONLY BENEATH THIS POINT ######


@click.group()
def cli():
    pass


cli.add_command(db)
cli.add_command(user)
cli.add_command(frontend)
cli.add_command(ember)
cli.add_command(celery)
cli.add_command(suite)


@cli.command(name='docker-start')
@click.option('-p', '--port', default=8000, type=int)
def docker_start(port):
    from flask_app.app import create_app
    from flask_app.models import db
    import flask_migrate
    import gunicorn.app.base

    _ensure_conf()

    app = create_app(config={'PROPAGATE_EXCEPTIONS': True})

    flask_migrate.Migrate(app, db)

    with app.app_context():
        flask_migrate.upgrade()

    workers_count = (multiprocessing.cpu_count() * 2) + 1

    class StandaloneApplication(gunicorn.app.base.BaseApplication):

        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super(StandaloneApplication, self).__init__()

        def load_config(self):
            config = dict([(key, value) for key, value in self.options.items()
                           if key in self.cfg.settings and value is not None])
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    options = {
        'bind': f'0.0.0.0:{port}',
        'workers': workers_count,
        'capture_output': True,
        'timeout': 70,
    }
    logbook.StderrHandler(level=logbook.DEBUG).push_application()
    if app.config['TESTING']:
        logbook.warning('Testing mode is active!')
    StandaloneApplication(app, options).run()



@cli.command(name='docker-nginx-start')
@click.option('--only-print', is_flag=True, default=False)
def docker_nginx_start(only_print):
    import jinja2
    with open('etc/nginx-site-conf.j2') as f:
        template = jinja2.Template(f.read())

    environ = defaultdict(str, os.environ)
    template_args = {'environ': environ, 'hostname': environ['BACKSLASH_HOSTNAME']}
    template_args['additional_routes'] = _parse_environment_routes()
    config = template.render(**template_args)
    if only_print:
        print(config)
        return

    with open('/etc/nginx/conf.d/backslash.conf', 'w') as f:
        f.write(config)

    nginx_path = '/usr/sbin/nginx'
    os.execv(nginx_path, [nginx_path, '-g', 'daemon off;'])


def _parse_environment_routes():
    rule_string = os.environ.get('BACKSLASH_ADDITIONAL_ROUTES')
    if rule_string:
        returned = [rule.split(':', 1) for rule in rule_string.split(',')]
        for rule in returned:
            assert len(rule) == 2, 'Invalid additional routes specified: {!r}'.format(rule_string)
        return returned
    return []


def _ensure_conf():
    config_directory = os.environ.get('CONFIG_DIRECTORY')
    assert config_directory, 'Configuration directory not specified through CONFIG_DIRECTORY'

    private_filename = os.path.join(config_directory, '000-private.yml')
    if not os.path.isfile(private_filename):
        with open(private_filename, 'w') as f:
            for secret_name in ('SECRET_KEY', 'SECURITY_PASSWORD_SALT'):
                f.write('{}: {!r}\n'.format(secret_name, _generate_secret_string()))

def _generate_secret_string(length=50):
    return "".join([random.choice(string.ascii_letters) for i in range(length)])


@cli.command()
@click.option('-p', '--port', default=8000, envvar='TESTSERVER_PORT')
@click.option('--tmux/--no-tmux', is_flag=True, default=True)
def testserver(tmux, port):
    if tmux:
        return _run_tmux_frontend(port=port)
    from flask_app.app import create_app

    extra_files=[
        from_project_root("flask_app", "app.yml")
    ]

    app = create_app({'DEBUG': True, 'TESTING': True, 'SECRET_KEY': 'dummy', 'SECURITY_PASSWORD_SALT': 'dummy'})
    logbook.StreamHandler(sys.stderr, level='DEBUG').push_application()
    logbook.compat.redirect_logging()
    app.run(port=port, extra_files=extra_files, use_reloader=False)

def _run_tmux_frontend(port):
    tmuxp = os.path.join(os.path.dirname(sys.executable), 'tmuxp')
    os.execve(tmuxp, [tmuxp, 'load', from_project_root('_lib', 'frontend_tmux.yml')], dict(os.environ, TESTSERVER_PORT=str(port), CONFIG_DIRECTORY=from_project_root("conf.d")))


@cli.command()
def unittest():
    _run_unittest()


def _run_unittest():
    subprocess.check_call(
        [sys.executable, '-m', "pytest", "tests/", "--cov=flask_app", "--cov-report=html"], cwd=from_project_root())


@cli.command()
@click.argument('pytest_args', nargs=-1)
def pytest(pytest_args):
    _run_pytest(pytest_args)


def _run_pytest(pytest_args=()):
    subprocess.check_call(
        [sys.executable, '-m', "pytest"]+list(pytest_args), cwd=from_project_root())


@cli.command()
def fulltest():
    _run_fulltest()


def _run_fulltest(extra_args=()):
    subprocess.check_call([sys.executable, '-m', "pytest", "tests"]
                          + list(extra_args), cwd=from_project_root())



@cli.command()
def shell():
    from flask_app.app import create_app
    from flask_app import models

    app = create_app({'SQLALCHEMY_ECHO': True})

    with app.app_context():
        interact({
            'app': app,
            'models': models,
            'db': models.db,
        })



if __name__ == "__main__":
    try:
        cli()
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
