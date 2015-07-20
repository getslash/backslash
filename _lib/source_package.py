#! /usr/bin/python
import os
import subprocess

from .bootstrapping import from_project_root
from .frontend import build_frontend

tarfile = from_project_root("src_pkg.tar.gz")

def _is_any_file_newer(paths, reference_filename):
    file_mtime = os.stat(reference_filename).st_mtime
    for path in paths:
        if os.stat(from_project_root(path)).st_mtime > file_mtime:
            return True
    return False

def _tar(paths):
    if 0 != subprocess.call("tar cvfz {0} {1}".format(tarfile, " ".join(paths)), shell=True, cwd=from_project_root()):
        raise Exception("Tar failed")

def _get_paths_to_tar(include_frontend):
    p = subprocess.Popen("git ls-files", stdout=subprocess.PIPE, cwd=from_project_root(), shell=True)
    returned = set()
    for subpath in p.stdout.readlines():
        subpath = subpath.decode('UTF-8')
        subpath = subpath.strip()
        returned.add(subpath)
    if 0 != p.wait():
        raise RuntimeError("git ls-files failed")
    if include_frontend:
        returned.add('static')
    return returned

def prepare_source_package(include_frontend=True):
    if include_frontend:
        build_frontend(False, True)
    paths = _get_paths_to_tar(include_frontend)
    if not os.path.exists(tarfile) or \
       _is_any_file_newer(paths, tarfile):
        _tar(paths)
    return tarfile
