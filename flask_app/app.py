import flask
import os
import yaml
from flask_security import Security
from flask_mail import Mail
import logbook
from logbook.compat import redirect_logging


def create_app(config=None):
    if config is None:
        config = {}

    ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

    app = flask.Flask(__name__, static_folder=os.path.join(ROOT_DIR, "..", "static"))

    _CONF_D_PATH = os.environ.get('CONFIG_DIRECTORY', os.path.join(ROOT_DIR, "..", "..", "conf.d"))

    configs = [os.path.join(ROOT_DIR, "app.yml")]

    if os.path.isdir(_CONF_D_PATH):
        configs.extend(sorted(os.path.join(_CONF_D_PATH, x) for x in os.listdir(_CONF_D_PATH) if x.endswith(".yml")))

    configs.append(os.path.expanduser('~/.config/backslash/devconfig.yml'))

    for yaml_path in configs:
        if os.path.isfile(yaml_path):
            with open(yaml_path) as yaml_file:
                app.config.update(yaml.load(yaml_file))

    app.config.update(config)

    if 'SQLALCHEMY_DATABASE_URI' not in app.config:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.path.expandvars(
            os.environ.get('SQLALCHEMY_DATABASE_URI', 'postgresql://localhost/{0}'.format(app.config['app_name'])))


    if os.path.exists("/dev/log"):
        syslog_handler = logbook.SyslogHandler(app.config['app_name'], "/dev/log")
        syslog_handler.push_application()

    del app.logger.handlers[:]
    redirect_logging()

    if app.config['TESTING']:
        app.config['TRACEBACK_DIR'] = '/tmp/backslash_tracebacks'
    else:
        _disable_logs(['dogpile.lock'])

    app.logger.info("Started")

    Mail(app)

    from . import models
    from .blueprints import rest, views, runtoken
    from .blueprints.api.main import blueprint as api_blueprint

    models.db.init_app(app)

    from . import auth
    Security(app, auth.user_datastore, register_blueprint=False)

    blueprints = [auth.auth, views.blueprint, api_blueprint, rest.blueprint, runtoken.blueprint]

    from .errors import errors

    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    for code in errors:
        app.errorhandler(code)(errors[code])

    return app


def _disable_logs(logger_names):

    logger_names = set(logger_names)

    def filter(record, _):
        return record.channel in logger_names

    logbook.NullHandler(filter=filter).push_application()
