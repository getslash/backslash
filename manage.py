import os
import functools
from flask.ext.script import Manager
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask_app.app import app
from flask_app.models import db

manager = Manager(app)

@manager.command
def create_db():
    db.create_all()

_FROM_HERE = functools.partial(os.path.join, os.path.dirname(__file__))

@manager.command
def testserver():
    app.config["DEBUG"] = True
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "dummy secret key"
    toolbar = DebugToolbarExtension(app)
    app.run(port=8000, extra_files=[
        _FROM_HERE("flask_app", "app.yml")
    ])

if __name__ == '__main__':
    manager.run()
