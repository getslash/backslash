#! /usr/bin/python
from __future__ import print_function
import os
import time
import random
import string
import subprocess


from _lib.bootstrapping import bootstrap_env, from_project_root, requires_env, from_env_bin
bootstrap_env(["base"])


from _lib.params import APP_NAME
from _lib.frontend import frontend
from _lib.source_package import prepare_source_package
from _lib.deployment import generate_nginx_config, run_uwsgi
from _lib.docker import build_docker_image, start_docker_container, stop_docker_container
from _lib.db import db
import click
import requests


##### ACTUAL CODE ONLY BENEATH THIS POINT ######


@click.group()
def cli():
    pass


cli.add_command(run_uwsgi)
cli.add_command(generate_nginx_config)
cli.add_command(db)
cli.add_command(frontend)

@cli.command('ensure-secret')
@click.argument("conf_file")
def ensure_secret(conf_file):
    dirname = os.path.dirname(conf_file)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    if os.path.exists(conf_file):
        return
    with open(conf_file, "w") as f:
        secret_key = "".join([random.choice(string.ascii_letters) for i in range(50)])
        print('SECRET_KEY: "{0}"'.format(secret_key), file=f)

@cli.command()
@click.option("--develop", is_flag=True)
@click.option("--app", is_flag=True)
def bootstrap(develop, app):
    deps = ["base"]
    if develop:
        deps.append("develop")
    if app:
        deps.append("app")
    bootstrap_env(deps)
    click.echo(click.style("Environment up to date", fg='green'))


@cli.command()
@requires_env("app")
def testserver():
    from flask_app.app import app
    app.config["DEBUG"] = True
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "dummy secret key"
    app.run(port=8000, extra_files=[
        from_project_root("flask_app", "app.yml")
    ])


@cli.command()
@click.option("--dest", type=click.Choice(["production", "staging", "localhost", "vagrant"]), help="Deployment target", required=True)
def deploy(dest):
    _run_deploy(dest)


def _run_deploy(dest):
    prepare_source_package()
    cmd = [from_env_bin("python"), from_env_bin("ansible-playbook"), "-i"]
    click.echo(click.style("Running deployment on {0!r}. This may take a while...".format(dest), fg='magenta'))

    cmd.append(from_project_root("ansible", "inventories", dest))
    if dest in ("localhost",):
        cmd.extend(["-c", "local"])
        if dest == "localhost":
            cmd.append("--sudo")
    cmd.append(from_project_root("ansible", "site.yml"))

    if dest == "vagrant":
        subprocess.check_call('vagrant up', shell=True)

        os.environ["ANSIBLE_HOST_KEY_CHECKING"] = 'false'
    subprocess.check_call(cmd)


@cli.command()
def unittest():
    _run_unittest()


@requires_env("app", "develop")
def _run_unittest():
    subprocess.check_call(
        [from_env_bin("py.test"), "tests/test_ut"], cwd=from_project_root())


@cli.command()
def fulltest():
    _run_fulltest()


@requires_env("app", "develop")
def _run_fulltest(extra_args=()):
    subprocess.check_call([from_env_bin("py.test"), "tests"]
                          + list(extra_args), cwd=from_project_root())


@cli.command('travis-test')
def travis_test():
    subprocess.check_call('createdb backslash', shell=True)
    _run_unittest()
    subprocess.check_call('dropdb backslash', shell=True)
    _run_deploy('localhost')
    _wait_for_travis_availability()
    _run_fulltest(["--www-port=80"])


def _wait_for_travis_availability():
    click.echo(click.style("Waiting for service to become available on travis", fg='magenta'))
    time.sleep(10)
    for retry in range(10):
        click.echo("Checking service...")
        resp = requests.get("http://localhost/")
        click.echo("Request returned {0}".format(resp.status_code))
        if resp.status_code == 200:
            break
        time.sleep(5)
    else:
        raise RuntimeError("Web service did not become responsive")
    click.echo(click.style("Service is up", fg='green'))


@cli.group()
def docker():
    pass

@docker.command()
def build():
    _run_docker_build()

def _run_docker_build():
    prepare_source_package()
    build_docker_image(tag=APP_NAME, root=from_project_root())

@docker.command()
@click.option("-p", "--port", default=80, type=int)
def start(port):
    _run_docker_start(port)

def _run_docker_start(port):
    persistent_dir = from_project_root('persistent')
    if not os.path.isdir(persistent_dir):
        os.makedirs(persistent_dir)
    db_container_name = _db_container_name()
    start_docker_container(image='postgres', name=db_container_name,
                           binds={os.path.join(persistent_dir, "db"):'/var/lib/postgresql/data'})
    container_name = _webapp_container_name()
    start_docker_container(image=APP_NAME, name=container_name, binds={persistent_dir:'/persistent'},
                           port_bindings={80: port},
                           links={db_container_name: 'db'})

@docker.command()
def stop():
    stop_docker_container(_webapp_container_name())

def _webapp_container_name():
    return '{0}-container'.format(APP_NAME)

def _db_container_name():
    return '{0}-db'.format(APP_NAME)

if __name__ == "__main__":
    cli()
