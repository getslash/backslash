#! /usr/bin/python
import os
import subprocess

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
tarfile = os.path.join(root_dir, "src_pkg.tar")

def _is_any_file_newer(paths, reference_filename):
    file_mtime = os.stat(reference_filename).st_mtime
    for path in paths:
        if os.stat(os.path.join(root_dir, path)).st_mtime > file_mtime:
            return True
    return False

def _tar(paths):
    if 0 != subprocess.call("tar cvf {0} {1}".format(tarfile, " ".join(paths)), shell=True, cwd=root_dir):
        raise Exception("Tar failed")

def _get_paths_to_tar():
    p = subprocess.Popen("git ls-files", stdout=subprocess.PIPE, cwd=root_dir, shell=True)
    returned = set()
    for subpath in p.stdout.readlines():
        subpath = subpath.strip()
        returned.add(os.path.dirname(subpath))
        returned.add(subpath)
    if 0 != p.wait():
        raise RuntimeError("git ls-files failed")
    return returned

if __name__ == '__main__':
    paths = _get_paths_to_tar()
    if not os.path.exists(tarfile) or \
       _is_any_file_newer(paths, tarfile):
        _tar(paths)
