from __future__ import absolute_import
from __future__ import print_function

import os
import shutil
import subprocess
from contextlib import contextmanager
from tempfile import mkdtemp, mkstemp

from .bootstrapping import from_project_root
from .source_package import prepare_source_package
from .params import APP_NAME

import yaml
from jinja2 import Template


def build_docker_image(root, tag):

    with _get_temp_path() as path:
        _generate_dockerfile(os.path.join(path, "Dockerfile"))
        _generate_supervisor_conf(os.path.join(path, "weber.conf"))
        shutil.copy(prepare_source_package(), path)

        subprocess.check_call(
            "docker build -t {0} .".format(tag), shell=True, cwd=path)

@contextmanager
def _get_temp_path():
    path = mkdtemp()
    try:
        yield path
    finally:
        shutil.rmtree(path)


def _generate_supervisor_conf(path):
    with open(os.path.join(os.path.dirname(__file__), "../ansible/roles/webapp/templates/supervisor.j2"), "r") as f:
        template = Template(f.read())

    with open(path, "w") as outfile:
        outfile.write(template.render(
            app_name=APP_NAME,
            deploy_root="/src",
            user_name="root",
        ))


def _generate_dockerfile(path):
    with open(os.path.join(os.path.dirname(__file__), "Dockerfile.j2"), "r") as f:
        template = Template(f.read())

    with open(path, "w") as outfile:
        outfile.write(template.render(
            apt_packages=' '.join(_get_apt_packages_from_ansible()),
            pip_packages=' '.join(repr(x) for x in _get_pip_dependencies()))
        )


def _get_apt_packages_from_ansible():
    vars_file = from_project_root('ansible', 'roles', 'common', 'vars', 'main.yml')
    with open(vars_file) as f:
        config = yaml.load(f)
    return config['required_packages']


def _get_pip_dependencies():
    deps = set()
    for dep in ('base', 'app'):
        with open(from_project_root('deps', dep + '.txt')) as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or not line:
                    continue
                deps.add(line)
    return sorted(deps)


class Compose(object):
    _COMPOSE_EXE = "docker-compose"

    def __init__(self, persistent_dir=None, port_bindings=None):
        super(Compose, self).__init__()
        self._persistent_dir = persistent_dir
        self._port_bindings = port_bindings or {}
        self._compose_file = None

    @staticmethod
    def _get_compose_template():
        with open(os.path.join(os.path.dirname(__file__), "docker-compose.yml.j2"), "r") as f:
            return Template(f.read())

    def __enter__(self):
        fd, path = mkstemp()
        self._compose_file = os.fdopen(fd, "w"), path
        template = self._get_compose_template()
        self._compose_file[0].write(template.render(
            tag=APP_NAME, persistent_dir=self._persistent_dir, port_bindings=self._port_bindings))
        self._compose_file[0].flush()
        return self

    def __exit__(self, _a, _b, _c):
        self._compose_file[0].close()
        os.unlink(self._compose_file[1])

    def run(self, args):
        subprocess.check_call([self._COMPOSE_EXE, "-f", self._compose_file[1], "-p", APP_NAME] + args)


def start_docker_container(persistent_dir, port_bindings=None):
    with Compose(persistent_dir=persistent_dir, port_bindings=port_bindings) as compose:
        compose.run(["up", "-d"])

def stop_docker_container():
    with Compose() as compose:
        compose.run(["stop"])
