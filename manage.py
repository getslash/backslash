#! /usr/bin/python
import os
import time
import subprocess

from _lib.bootstrapping import bootstrap_env, from_project_root, requires_env, from_env_bin
bootstrap_env(["base"])


from _lib.source_package import prepare_source_package
import click
import logbook
import requests

_logger = logbook.Logger(__name__)


##### ACTUAL CODE ONLY BENEATH THIS POINT ######


@click.group()
def cli():
    pass


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

    cmd.append(from_project_root("ansible", "inventories", dest))
    if dest == "localhost":
        cmd.extend(["-c", "local", "--sudo"])
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
    _run_unittest()
    _run_deploy('localhost')
    _wait_for_travis_availability()
    _run_fulltest(["--www-port=80"])


def _wait_for_travis_availability():
    _logger.info("Waiting for service to become available on travis")
    for retry in range(10):
        _logger.debug("Checking service...")
        resp = requests.get("http://localhost/")
        _logger.debug("Request returned {0}", resp.status_code)
        if resp.status_code == 200:
            break
        time.sleep(5)
    else:
        raise RuntimeError("Web service did not become responsive")
    _logger.info("Service is up")


if __name__ == "__main__":
    cli()
