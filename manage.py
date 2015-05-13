#! /usr/bin/python
from __future__ import print_function
import os
import sys
import time
import random
import string
import subprocess


from _lib.bootstrapping import bootstrap_env, from_project_root, requires_env, from_env_bin
from _lib.ansible import ensure_ansible
bootstrap_env(["base"])


from _lib.params import APP_NAME
from _lib.source_package import prepare_source_package
from _lib.deployment import generate_nginx_config, run_uwsgi
from _lib.docker import build_docker_image, start_docker_container, stop_docker_container
from _lib.db import db
from _lib.utils import interact
import click
import requests
import logbook

##### ACTUAL CODE ONLY BENEATH THIS POINT ######


@click.group()
def cli():
    pass


cli.add_command(run_uwsgi)
cli.add_command(generate_nginx_config)
cli.add_command(db)

@cli.command('ensure-secret')
@click.argument("conf_file")
def ensure_secret(conf_file):
    dirname = os.path.dirname(conf_file)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    if os.path.exists(conf_file):
        return
    with open(conf_file, "w") as f:
        print('SECRET_KEY: "{0}"'.format(_generate_secret()), file=f)
        print('SECURITY_PASSWORD_SALT: "{0}"'.format(_generate_secret()), file=f)

def _generate_secret(length=50):
    return "".join([random.choice(string.ascii_letters) for i in range(length)])

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
@click.option('--livereload/--no-livereload', is_flag=True, default=True)
@requires_env("app", "develop")
@click.option('--tmux/--no-tmux', is_flag=True, default=True)
def testserver(tmux, livereload, port=8000):
    if tmux:
        return _run_tmux_frontend()
    from flask_app.app import create_app
    app = create_app({'DEBUG': True, 'TESTING': True, 'SECRET_KEY': 'dummy', 'SECURITY_PASSWORD_SALT': 'dummy'})

    extra_files=[
        from_project_root("flask_app", "app.yml")
    ]

    app = create_app({'DEBUG': True, 'TESTING': True, 'SECRET_KEY': 'dummy'})
    if livereload:
        from livereload import Server
        s = Server(app)
        for filename in extra_files:
            s.watch(filename)
        s.watch('flask_app')
        logbook.StreamHandler(sys.stderr, level='DEBUG').push_application()
        s.serve(port=port, liveport=35729)
    else:
        app.run(port=port, extra_files=extra_files)

def _run_tmux_frontend():
    tmuxp = from_env_bin('tmuxp')
    os.execv(tmuxp, [tmuxp, 'load', from_project_root('_lib', 'frontend_tmux.yml')])

@cli.command()
@click.option("--dest", type=click.Choice(["production", "staging", "localhost", "vagrant"]), help="Deployment target", required=True)
@click.option("--sudo/--no-sudo", default=False)
@click.option("--ask-sudo-pass/--no-ask-sudo-pass", default=False)
def deploy(dest, sudo, ask_sudo_pass):
    _run_deploy(dest, sudo, ask_sudo_pass)


def _run_deploy(dest, sudo=False, ask_sudo_pass=False):
    prepare_source_package()
    ansible = ensure_ansible()
    click.echo(click.style("Running deployment on {0!r}. This may take a while...".format(dest), fg='magenta'))

    if dest == "vagrant":
        # Vagrant will invoke ansible
        environ = os.environ.copy()
        environ["PATH"] = "{}:{}".format(os.path.dirname(ansible), environ["PATH"])
        # "vagrant up --provision" doesn't call provision if the virtual machine is already up,
        # so we have to call vagrant provision explicitly
        subprocess.check_call('vagrant up', shell=True, env=environ)
        subprocess.check_call('vagrant provision', shell=True, env=environ)
    else:
        cmd = [ansible, "-i",
               from_project_root("ansible", "inventories", dest)]
        if dest in ("localhost",):
            cmd.extend(["-c", "local"])
            if dest == "localhost":
                cmd.append("--sudo")

        if sudo:
            cmd.append('--sudo')

        if ask_sudo_pass:
            cmd.append('--ask-sudo-pass')

        cmd.append(from_project_root("ansible", "site.yml"))
        subprocess.check_call(cmd)


@cli.command()
def unittest():
    _run_unittest()


@requires_env("app", "develop")
def _run_unittest():
    subprocess.check_call(
        [from_env_bin("py.test"), "tests/test_ut"], cwd=from_project_root())


@cli.command()
@click.argument('pytest_args', nargs=-1)
def pytest(pytest_args):
    _run_pytest(pytest_args)


@requires_env("app", "develop")
def _run_pytest(pytest_args=()):
    subprocess.check_call(
        [from_env_bin("py.test")]+list(pytest_args), cwd=from_project_root())


@cli.command()
def fulltest():
    _run_fulltest()


@requires_env("app", "develop")
def _run_fulltest(extra_args=()):
    subprocess.check_call([from_env_bin("py.test"), "tests"]
                          + list(extra_args), cwd=from_project_root())


@cli.command('travis-test')
def travis_test():
    subprocess.check_call('createdb {0}'.format(APP_NAME), shell=True)
    _run_unittest()
    subprocess.check_call('dropdb {0}'.format(APP_NAME), shell=True)
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
    start_docker_container(persistent_dir=persistent_dir, port_bindings={80: port})

@docker.command()
def stop():
    stop_docker_container()

def _db_container_name():
    return '{0}-db'.format(APP_NAME)

@cli.command()
@requires_env("app", "develop")
def shell():
    from flask_app.app import create_app
    from flask_app import models

    app = create_app()

    with app.app_context():
        interact({
            'db': db,
            'app': app,
            'models': models,
            'db': models.db,
        })


if __name__ == "__main__":
    cli()
