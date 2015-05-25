import os
import sys
from multiprocessing import cpu_count

import click

from .bootstrapping import from_env, from_env_bin, requires_env, from_project_root
from .params import APP_NAME

_UNIX_SOCKET_NAME = "/tmp/__{0}_uwsgi.sock".format(APP_NAME)


@click.option("--catch-exceptions", is_flag=True)
@click.command()
@requires_env("app")
def run_uwsgi(catch_exceptions):
    uwsgi_bin = from_env_bin("uwsgi")
    cmd = [uwsgi_bin, "-b", "16384", "--chmod-socket=666",
           "--home", from_env(), "--pythonpath", from_project_root(), "--module=flask_app.wsgi", "--callable=app",
           "-s", _UNIX_SOCKET_NAME, "-p", str(cpu_count()), "--master"]
    if catch_exceptions:
        cmd.append("--catch-exceptions")
    os.execv(uwsgi_bin, cmd)

@click.command()
@click.argument('path')
def generate_nginx_config(path):
    if not os.path.isdir(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, "w") as f:
        f.write("""server {{

    location /static {{
       alias {static_root};
    }}

    location = / {{
       rewrite ^/$ /static/index.html;
    }}

    location / {{
       	 include uwsgi_params;
         uwsgi_pass unix:{sock_name};
    }}
}}""".format(static_root=from_project_root("static"), sock_name=_UNIX_SOCKET_NAME))
