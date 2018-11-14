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


def which(bin):
    for directory in os.environ['PATH'].split(':'):
        full_path = os.path.join(directory, bin)
        if os.path.isfile(full_path):
            return full_path

    raise ValueError('Could not find a python interpreter named {}'.format(bin))
