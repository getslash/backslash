from __future__ import absolute_import
from __future__ import print_function

import os
import shutil
import subprocess
from contextlib import contextmanager
from tempfile import mkdtemp

from .bootstrapping import from_project_root
from .source_package import prepare_source_package

import logbook
import yaml
import docker

_docker = None


def get_docker_client():
    global _docker
    if _docker is None:
        _docker = docker.Client(version='1.11')
    return _docker


def build_docker_image(root, tag):

    with _get_temp_path() as path:
        _generate_dockerfile(os.path.join(path, "Dockerfile"))

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


def _generate_dockerfile(path):
    with open(path, "w") as outfile:
        for line in _generate_dockerfile_lines():
            print(line, file=outfile)

def _generate_dockerfile_lines():
    yield FROM('ubuntu:14.04')
    yield RUN('apt-get update')
    yield RUN('apt-get install -y', ' '.join(_get_apt_packages_from_ansible()))
    yield RUN('apt-add-repository ppa:nginx/stable')
    yield RUN('apt-get update')
    yield RUN('apt-get install -y nginx')
    yield RUN('wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python')
    yield RUN('easy_install pip')
    yield RUN('pip install virtualenv')

    # configure virtualenv and install dependencies so that it will get cached by docker
    yield RUN('virtualenv /env')
    yield ENV('VIRTUALENV_PATH', '/env')
    yield RUN('/env/bin/pip install', ' '.join(repr(x) for x in _get_pip_dependencies()))

    # set up configuration
    yield RUN('mkdir /src /persistent /persistent/config')
    yield ENV('CONFIG_DIRECTORY /persistent/config')

    # untar sources
    yield ADD('./src_pkg.tar /tmp/')
    yield RUN('cd /src && tar xvf /tmp/src_pkg.tar')
    yield RUN('cd /src && rm -rf .env && find . -name "*.pyc" -delete')
    yield RUN('cd /src && python manage.py bootstrap --app')
    yield RUN('rm -rf /etc/nginx/sites-enabled/*')
    yield RUN('cd /src && python manage.py generate_nginx_config /etc/nginx/sites-enabled/webapp')
    yield EXPOSE('80')
    yield CMD('service nginx start && cd /src && python manage.py ensure-secret /persistent/config/000-secret.yml && python manage.py run_uwsgi')



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



def start_docker_container(image, name, binds, port_bindings):
    docker = get_docker_client()
    container = _try_get_container(name, only_running=False)
    if container is not None:
        if container['running']:
            logbook.info(
                "Container {} already running. Not doing anything...", container['Id'])
            return container['Id']

        logbook.info("Removing dead container {}", container['Id'])
        docker.remove_container(container['Id'])

    container = docker.create_container(
        image=image,
        detach=True,
        name=name)
    docker.start(name, binds=binds, port_bindings=port_bindings)
    logbook.info("Container started. Id: {}", container['Id'])
    return container['Id']

def stop_docker_container(name):
    running = _try_get_container(name)
    if running is not None:
        logbook.info("Stopping container {}", running['Id'])
        get_docker_client().stop(running['Id'])
    else:
        logbook.info("Container is not running. Not doing anything.")


def _try_get_container(container_name, only_running=True):
    for container in get_docker_client().containers(all=not only_running):
        container['running'] = bool(
            container['Status']) and 'exited' not in container['Status'].lower()
        if '/' + container_name in container['Names']:
            return container
    return None

def _terminate_docker_container(container_name):
    container = _try_get_container(container_name)
    if container is not None:
        get_docker_client().stop(container_name)


class DockerInstruction(object):

    def __init__(self, *args):
        super(DockerInstruction, self).__init__()
        self.args = args

    def __repr__(self):
        return '{0} {1}'.format(type(self).__name__, ' '.join(self.args))

class FROM(DockerInstruction):
    pass

class RUN(DockerInstruction):
    pass

class ADD(DockerInstruction):
    pass

class ENV(DockerInstruction):
    pass

class EXPOSE(DockerInstruction):
    pass

class CMD(DockerInstruction):
    pass
