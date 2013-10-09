#! /usr/bin/python
import os
import subprocess

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
tarfile = os.path.join(root_dir, "src_pkg.tar")

def _is_dir_newer(directory, filename):
    file_mtime = os.stat(filename).st_mtime
    for dirname, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".pyc"):
                continue
            if _is_file_newer(os.path.join(dirname, filename), file_mtime):
                return True
    return False

def _is_file_newer(filename, file_mtime):
    return os.stat(filename).st_mtime > file_mtime

def _tar():
    if 0 != subprocess.call("tar cvf {0} flask_app manage.py static".format(tarfile), shell=True, cwd=root_dir):
        raise Exception("Tar failed")

if __name__ == '__main__':
    if not os.path.exists(tarfile) or \
       _is_dir_newer(os.path.join(root_dir, "flask_app"), tarfile) or \
       _is_dir_newer(os.path.join(root_dir, "static"), tarfile) or \
       _is_file_newer(os.path.join(root_dir, "manage.py"), os.stat(tarfile).st_mtime):
        _tar()
