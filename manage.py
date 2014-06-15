#! /usr/bin/python
import os
import time
import subprocess

from _lib.bootstrapping import bootstrap_env, from_project_root, requires_env, from_env_bin
bootstrap_env(["base"])


from _lib.source_package import prepare_source_package
import click
import requests
import yaml

with open(from_project_root("flask_app", "app.yml")) as f:
    APP_NAME = yaml.load(f)["app_name"]


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
@click.option("--dest", type=click.Choice(["production", "staging", "localhost", "vagrant", "docker"]), help="Deployment target", required=True)
def deploy(dest):
    _run_deploy(dest)


def _run_deploy(dest):
    prepare_source_package()
    cmd = [from_env_bin("python"), from_env_bin("ansible-playbook"), "-i"]
    click.echo(click.style("Running deployment on {0!r}. This may take a while...".format(dest), fg='magenta'))

    cmd.append(from_project_root("ansible", "inventories", dest))
    if dest in ("localhost", "docker"):
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
    _run_unittest()
    if os.environ.get('USE_DOCKER', 'true').lower() == 'true':
        _run_docker_build()
        _run_docker_start(80)
    else:
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
    subprocess.check_call("docker build -t {0} .".format(APP_NAME), shell=True, cwd=from_project_root())

@docker.command()
@click.option("-p", "--port", default=80, type=int)
def start(port):
    _run_docker_start(port)

def _run_docker_start(port):
    subprocess.check_call("docker run -d --name {0}-container -p {1}:80 {0}".format(APP_NAME, port), shell=True)

@docker.command()
def stop():
    click.echo(click.style("Stopping container...", fg='magenta'))
    subprocess.check_call("docker stop {0}-container".format(APP_NAME), shell=True)
    subprocess.check_call("docker rm {0}-container".format(APP_NAME), shell=True)

if __name__ == "__main__":
    cli()
