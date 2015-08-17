import os
import sys
from multiprocessing import cpu_count

import click

from .bootstrapping import from_env, from_env_bin, requires_env, from_project_root
from .params import APP_NAME

_UNIX_SOCKET_NAME = "/var/run/{}/wsgi.sock".format(APP_NAME)


@click.command()
@requires_env("app")
def run_gunicorn():
    gunicorn_bin = from_env_bin('gunicorn')
    cmd = [gunicorn_bin, '--log-syslog', '-b', 'unix://{}'.format(_UNIX_SOCKET_NAME), 'flask_app.wsgi:app', '--chdir', from_project_root('.')]
    os.execv(gunicorn_bin, cmd)

@click.command()
@click.argument('path')
def generate_nginx_config(path):
    if not os.path.isdir(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, "w") as f:
        f.write("""server {{
    listen 80;
    location /static {{
       alias {static_root};
    }}

    location = / {{
       rewrite ^/$ /static/index.html;
    }}

    location / {{
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://unix:{sock_name};
    }}
}}""".format(static_root=from_project_root("static"), sock_name=_UNIX_SOCKET_NAME))
