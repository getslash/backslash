import os
import subprocess
import sys
from contextlib import contextmanager

import logbook

import click

from .bootstrapping import from_env, from_project_root


_NPM_PREFIX = from_project_root('.env/npm')
_EMBER_EXECUTABLE = os.path.join(_NPM_PREFIX, 'bin', 'ember')
_BOWER_EXECUTABLE = os.path.join(_NPM_PREFIX, 'bin', 'bower')

_logger = logbook.Logger(__name__)


@click.command()
@click.argument('args', nargs=-1)
def ember(args):
    args = [_EMBER_EXECUTABLE] + list(args)
    _bootstrap_frontend()
    _execute(' '.join(args), cwd=from_project_root('webapp'))


@click.group()
def frontend():
    pass

@frontend.command()
@click.option("--watch", is_flag=True)
@click.option("--production", is_flag=True)
def build(watch, production):
    return build_frontend(watch, production)

def build_frontend(watch, production):
    _bootstrap_frontend()
    cmd = '{} build --output-path=../static/'.format(_EMBER_EXECUTABLE)
    if watch:
        cmd += ' --watch'
    if production:
        cmd += ' --environment=production'
    _execute(cmd)

def _bootstrap_frontend():
    with _get_timestamp_update_context(
            from_env("frontend.timestamp"), ["webapp/package.json"]) as uptodate:
        if not uptodate:
            _logger.info("Bootstrapping frontend environment...")
            _execute("npm install -g ember-cli bower")
            _execute("npm install")
            _execute("{} install --allow-root".format(_BOWER_EXECUTABLE))

@contextmanager
def _get_timestamp_update_context(timestamp_path, paths):
    timestamp = _get_timestamp(timestamp_path)
    path_timestamps = [_get_timestamp(from_project_root(p))
                       for p in paths]
    uptodate = timestamp != 0 and timestamp > max(path_timestamps)
    yield uptodate
    with open(timestamp_path, "w"):
        pass

def _execute(cmd, cwd=None):
    if cwd is None:
        cwd = from_project_root('webapp')
    env = os.environ.copy()
    env['NPM_CONFIG_PREFIX'] = _NPM_PREFIX
    returncode = subprocess.call(cmd, shell=True, cwd=cwd, env=env)
    if returncode != 0:
        sys.exit(returncode)

def _get_timestamp(path):
    try:
        return os.stat(path).st_mtime
    except OSError:
        return 0
