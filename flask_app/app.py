import flask
import logging
import os
import sys
import yaml
from flask.ext.security import Security
from flask.ext.mail import Mail

import logbook

def create_app(config=None):
    if config is None:
        config = {}

    ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

    app = flask.Flask(__name__, static_folder=os.path.join(ROOT_DIR, "..", "static"))


    app.config['SQLALCHEMY_DATABASE_URI'] = os.path.expandvars(
    os.environ.get('SQLALCHEMY_DATABASE_URI', 'postgresql://localhost/backslash'))

    _CONF_D_PATH = os.environ.get('CONFIG_DIRECTORY', os.path.join(ROOT_DIR, "..", "conf.d"))

    configs = [os.path.join(ROOT_DIR, "app.yml")]

    if os.path.isdir(_CONF_D_PATH):
        configs.extend(sorted(os.path.join(_CONF_D_PATH, x) for x in os.listdir(_CONF_D_PATH) if x.endswith(".yml")))

    for yaml_path in configs:
        if os.path.isfile(yaml_path):
            with open(yaml_path) as yaml_file:
                app.config.update(yaml.load(yaml_file))

    app.config.update(config)

    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(console_handler)

    logbook.info("Started")

    Mail(app)

    from . import models
    from . import api
    from . import rest
    from . import errors
    from . import views

    models.db.init_app(app)

    from . import auth
    Security(app, auth.user_datastore)

    from .auth import auth
    from .views import views
    from .setup import setup
    blueprints = [auth, views, setup, api.blueprint, rest.blueprint]

    from .errors import errors

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    for code in errors:
        app.errorhandler(code)(errors[code])

    return app
