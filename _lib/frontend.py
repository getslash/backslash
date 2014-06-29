import os
import subprocess
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
def build(watch):
    _bootstrap_npm()
    if watch:
        _execute("gulp watch")
    else:
        _execute("gulp")

def _bootstrap_npm():
    with _get_timestamp_update_context(
            from_env("npm.timestamp"), ["bower.json", "package.json"]) as uptodate:
        if not uptodate:
            _logger.info("Bootstrapping npm environment...")
            _execute("npm install")
            _execute("npm install gulp")
            _execute("npm install -g gulp")
            _execute("npm install -g bower")
            _execute("bower install --allow-root -f")

@contextmanager
def _get_timestamp_update_context(timestamp_path, paths):
    timestamp = _get_timestamp(timestamp_path)
    path_timestamps = [_get_timestamp(from_project_root(p))
                       for p in paths]
    uptodate = timestamp != 0 and timestamp > max(path_timestamps)
    yield uptodate
    with open(timestamp_path, "w"):
        pass

def _execute(cmd):
    subprocess.call(cmd, shell=True, cwd=from_project_root())

def _get_timestamp(path):
    try:
        return os.stat(path).st_mtime
    except OSError:
        return 0
