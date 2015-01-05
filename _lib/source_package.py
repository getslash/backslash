#! /usr/bin/python
import os
import subprocess

from .bootstrapping import from_project_root

tarfile = from_project_root("src_pkg.tar")

def _is_any_file_newer(paths, reference_filename):
    file_mtime = os.stat(reference_filename).st_mtime
    for path in paths:
        if os.stat(from_project_root(path)).st_mtime > file_mtime:
            return True
    return False

def _tar(paths):
    if 0 != subprocess.call("tar cvf {0} {1}".format(tarfile, " ".join(paths)), shell=True, cwd=from_project_root()):
        raise Exception("Tar failed")

def _get_paths_to_tar():
    p = subprocess.Popen("git ls-files", stdout=subprocess.PIPE, cwd=from_project_root(), shell=True)
    returned = set()
    for subpath in p.stdout.readlines():
        subpath = subpath.decode('UTF-8')
        subpath = subpath.strip()
        returned.add(os.path.dirname(subpath))
        returned.add(subpath)
    if 0 != p.wait():
        raise RuntimeError("git ls-files failed")
    return returned

def prepare_source_package():
    paths = _get_paths_to_tar()
    if not os.path.exists(tarfile) or \
       _is_any_file_newer(paths, tarfile):
        _tar(paths)
    return tarfile
