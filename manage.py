import functools
import os

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

from flask_app.app import app
from flask_app.models import db

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

_FROM_HERE = functools.partial(os.path.join, os.path.dirname(__file__))

@manager.command
def testserver():
    from flask.ext.debugtoolbar import DebugToolbarExtension
    app.config["DEBUG"] = True
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "dummy secret key"

    DebugToolbarExtension(app)
    app.run(port=8000, extra_files=[
        _FROM_HERE("flask_app", "app.yml")
    ])

if __name__ == '__main__':
    manager.run()
