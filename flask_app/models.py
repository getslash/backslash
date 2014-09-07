from .app import app
from flask.ext.sqlalchemy import SQLAlchemy

import datetime

db = SQLAlchemy(app)

### Add models here

class Session(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    end_time = db.Column(db.DateTime, default=None)
    hostname = db.Column(db.String(100))
