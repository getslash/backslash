from __future__ import absolute_import
import subprocess

import logbook
import docker

_docker = None


def get_docker_client():
    global _docker
    if _docker is None:
        _docker = docker.Client()
    return _docker


def build_docker_image(root, tag):
    subprocess.check_call(
        "docker build -t {0} .".format(tag), shell=True, cwd=root)


def start_docker_container(image, name, binds, port_bindings=(), links=()):
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
    docker.start(name, binds=binds, port_bindings=port_bindings, links=links)
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
