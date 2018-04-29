import functools
import os
import subprocess
import sys

PYTHON_INTERPRETER = os.path.abspath(sys.executable)

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_ENV_DIR = os.environ.get("VIRTUALENV_PATH", os.path.join(_PROJECT_ROOT, ".env"))

from_project_root = functools.partial(os.path.join, _PROJECT_ROOT)
from_env = functools.partial(os.path.join, _ENV_DIR)
from_env_bin = functools.partial(from_env, "bin")


def requires_env(*names):
    def decorator(func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            bootstrap_env(names)
            return func(*args, **kwargs)
        return new_func
    return decorator


def which(bin):
    for directory in os.environ['PATH'].split(':'):
        full_path = os.path.join(directory, bin)
        if os.path.isfile(full_path):
            return full_path

    raise ValueError('Could not find a python interpreter named {}'.format(bin))


def bootstrap_env(deps=("base",)):
    out_of_date = [dep for dep in deps if _is_dep_out_of_date(dep)]

    interpreter = which(PYTHON_INTERPRETER)

    if out_of_date:
        if not os.path.exists(from_env_bin("python")):
            subprocess.check_call("{} -m virtualenv {}".format(interpreter, _ENV_DIR), shell=True)
        cmd = "{}/bin/pip install".format(_ENV_DIR)
        for dep in out_of_date:
            cmd += " -r {}".format(_get_depfile_path(dep))
        subprocess.check_call(cmd, shell=True)
        for dep in deps:
            _mark_up_to_date(dep)

    python = os.path.abspath(os.path.join(_ENV_DIR, "bin", "python"))
    if os.path.abspath(sys.executable) != python:
        os.environ.pop('__PYVENV_LAUNCHER__', None)
        os.execv(python, [python] + sys.argv)


def _is_dep_out_of_date(dep):
    depfile_mtime = os.stat(_get_depfile_path(dep)).st_mtime
    try:
        timestamp = os.stat(_get_timestamp_path(dep)).st_mtime
    except OSError:
        timestamp = 0
    return depfile_mtime >= timestamp


def _get_depfile_path(dep):
    return os.path.join(_PROJECT_ROOT, "deps", dep + ".txt")


def _mark_up_to_date(dep):
    with open(_get_timestamp_path(dep), "w"):
        pass


def _get_timestamp_path(dep):
    return os.path.join(_ENV_DIR, "{}_dep_timestamp".format(dep))
