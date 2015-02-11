import os
import subprocess
from .bootstrapping import which

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_ENV_DIR = os.environ.get("VIRTUALENV_PATH", os.path.join(_PROJECT_ROOT, ".ansible-env"))
_PIP = os.path.join(_ENV_DIR, 'bin', 'pip')


def _ensure_env():
    if not os.path.isdir(_ENV_DIR):
        subprocess.check_call(['virtualenv', '-p', which('python2'), _ENV_DIR])


def ensure_ansible():
    _ensure_env()
    full_path = os.path.join(_ENV_DIR, 'bin', 'ansible-playbook')
    if not os.path.isfile(full_path):
        subprocess.check_call([_PIP, 'install', 'ansible>=1.2'])

    return full_path

