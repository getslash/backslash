#! /usr/bin/python
from __future__ import print_function
import os
import time
import random
import string
import subprocess


from _lib.bootstrapping import bootstrap_env, from_project_root, requires_env, from_env_bin
from _lib.ansible import ensure_ansible
bootstrap_env(["base"])


from _lib.source_package import prepare_source_package
from _lib.deployment import run_gunicorn
import click
import requests


##### ACTUAL CODE ONLY BENEATH THIS POINT ######


@click.group()
def cli():
    pass


cli.add_command(run_gunicorn)

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
@click.option('--livereload/--no-livereload', is_flag=True, default=True)
@click.option('-p', '--port', default=8000)
@requires_env("app", "develop")
def testserver(livereload, port):
    from flask_app.app import create_app

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
        s.serve(port=port, liveport=35729)
    else:
        app.run(port=port, extra_files=extra_files)


@cli.command()
@click.option("--dest", type=click.Choice(["production", "staging", "localhost", "vagrant"]), help="Deployment target", required=True)
@click.option("--vagrant-machine", type=str, default="", help="Vagrant machine to provision")
@click.option("--sudo/--no-sudo", default=False)
@click.option("--ask-sudo-pass/--no-ask-sudo-pass", default=False)
def deploy(dest, sudo, ask_sudo_pass, vagrant_machine):
    _run_deploy(dest, sudo, ask_sudo_pass, vagrant_machine)


def _run_deploy(dest, sudo=False, ask_sudo_pass=False, vagrant_machine=""):
    prepare_source_package()
    ansible = ensure_ansible()
    click.echo(click.style("Running deployment on {0!r}. This may take a while...".format(dest), fg='magenta'))

    if dest == "vagrant":
        # Vagrant will invoke ansible
        environ = os.environ.copy()
        environ["PATH"] = "{}:{}".format(os.path.dirname(ansible), environ["PATH"])
        # "vagrant up --provision" doesn't call provision if the virtual machine is already up,
        # so we have to call vagrant provision explicitly
        subprocess.check_call('vagrant up ' + vagrant_machine, shell=True, env=environ)
        subprocess.check_call('vagrant provision ' + vagrant_machine, shell=True, env=environ)
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
    _run_unittest()


def _wait_for_travis_availability():
    click.echo(click.style("Waiting for service to become available on travis", fg='magenta'))
    time.sleep(10)
    for _ in range(10):
        click.echo("Checking service...")
        resp = requests.get("http://localhost/")
        click.echo("Request returned {0}".format(resp.status_code))
        if resp.status_code == 200:
            break
        time.sleep(5)
    else:
        raise RuntimeError("Web service did not become responsive")
    click.echo(click.style("Service is up", fg='green'))


if __name__ == "__main__":
    cli()
