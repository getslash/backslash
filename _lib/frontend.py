import os
import subprocess
import sys
from contextlib import contextmanager

import logbook

import click

from .bootstrapping import from_env, from_project_root

_logger = logbook.Logger(__name__)


@click.group()
def frontend():
    pass

@frontend.command()
@click.option("--watch", is_flag=True)
@click.option("--production", is_flag=True)
def build(watch, production):
    _bootstrap_frontend()
    cmd = 'ember build --output-path=../static/'
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
            _execute("bower install --allow-root")

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
    returncode = subprocess.call(cmd, shell=True, cwd=cwd)
    if returncode != 0:
        sys.exit(returncode)

def _get_timestamp(path):
    try:
        return os.stat(path).st_mtime
    except OSError:
        return 0
