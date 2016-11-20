#! /usr/bin/python
from __future__ import print_function
import json
import os
import sys
import time
import random
import string
import subprocess
from contextlib import contextmanager

from _lib.bootstrapping import bootstrap_env, from_project_root, requires_env, from_env_bin
from _lib.ansible import ensure_ansible
bootstrap_env(["base"])


from _lib.params import APP_NAME
from _lib.frontend import frontend, ember, build_frontend
from _lib.source_package import prepare_source_package
from _lib.db import db
from _lib.users import user
from _lib.celery import celery
from _lib.slash_running import suite
from _lib.utils import interact
from _lib.deployment import run_gunicorn
import click
import requests
import logbook
import logbook.compat

##### ACTUAL CODE ONLY BENEATH THIS POINT ######


@click.group()
def cli():
    pass


cli.add_command(run_gunicorn)
cli.add_command(db)
cli.add_command(user)
cli.add_command(frontend)
cli.add_command(ember)
cli.add_command(celery)
cli.add_command(suite)

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
@click.option('-p', '--port', default=8000, envvar='TESTSERVER_PORT')
@click.option('--tmux/--no-tmux', is_flag=True, default=True)
@requires_env("app", "develop")
def testserver(tmux, livereload, port):
    if tmux:
        return _run_tmux_frontend(port=port)
    from flask_app.app import create_app

    extra_files=[
        from_project_root("flask_app", "app.yml")
    ]

    app = create_app({'DEBUG': True, 'TESTING': True, 'SECRET_KEY': 'dummy', 'SECURITY_PASSWORD_SALT': 'dummy'})
    if livereload:
        from livereload import Server
        s = Server(app)
        for filename in extra_files:
            s.watch(filename)
        s.watch('flask_app')
        for filename in ['webapp.js', 'vendor.js', 'webapp.css']:
            s.watch(os.path.join('static', 'assets', filename), delay=1)
        logbook.StreamHandler(sys.stderr, level='DEBUG').push_application()
        logbook.compat.redirect_logging()
        s.serve(port=port, liveport=35729)
    else:
        app.run(port=port, extra_files=extra_files)

def _run_tmux_frontend(port):
    tmuxp = from_env_bin('tmuxp')
    os.execve(tmuxp, [tmuxp, 'load', from_project_root('_lib', 'frontend_tmux.yml')], dict(os.environ, TESTSERVER_PORT=str(port), CONFIG_DIRECTORY=from_project_root("conf.d")))

@cli.command()
@click.option("--dest", type=click.Choice(["production", "staging", "localhost", "vagrant", "custom"]), help="Deployment target", required=True)
@click.option("-i", "--inventory", type=str, default=None, help="Path to an inventory file. Should be specified only when \"--dest custom\" is set")
@click.option("--vagrant-machine", type=str, default="", help="Vagrant machine to provision")
@click.option("--sudo/--no-sudo", default=False)
@click.option("--ask-sudo-pass/--no-ask-sudo-pass", default=False)
def deploy(dest, sudo, ask_sudo_pass, vagrant_machine, inventory):
    prepare_source_package()
    ansible = ensure_ansible()

    if dest == "vagrant":
        # Vagrant will invoke ansible
        environ = os.environ.copy()
        environ["PATH"] = "{}:{}".format(os.path.dirname(ansible), environ["PATH"])
        # "vagrant up --provision" doesn't call provision if the virtual machine is already up,
        # so we have to call vagrant provision explicitly
        click.echo(click.style("Running deployment on Vagrant. This may take a while...", fg='magenta'))
        subprocess.check_call('vagrant up ' + vagrant_machine, shell=True, env=environ)
        subprocess.check_call('vagrant provision ' + vagrant_machine, shell=True, env=environ)
    else:
        if dest == "custom":
            if inventory is None:
                raise click.ClickException("-i/--inventory should be specified together with \"--dest custom\"")
            if not os.path.exists(inventory):
                raise click.ClickException("Custom inventory file {} doesn't exist".format(inventory))
        else:
            if inventory is not None:
                raise click.ClickException("-i/--inventory should be specified only when \"--dest custom\" is specified")
            inventory = from_project_root("ansible", "inventories", dest)
        click.echo(click.style("Running deployment on {}. This may take a while...".format(inventory), fg='magenta'))
        cmd = [ansible, "-i", inventory]
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
        [from_env_bin("py.test"), "tests/", "--cov=flask_app", "--cov-report=html"], cwd=from_project_root())


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



@cli.command()
@requires_env("app", "develop")
def shell():
    from flask_app.app import create_app
    from flask_app import models

    app = create_app({'SQLALCHEMY_ECHO': True})

    with app.app_context():
        interact({
            'app': app,
            'models': models,
            'db': models.db,
        })



if __name__ == "__main__":
    try:
        cli()
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
