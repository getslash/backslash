import datetime

from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy.orm import backref

from .app import app
from .utils import get_current_time
from .rendering import computed_field

db = SQLAlchemy(app)

### Add models here

class Session(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, default=get_current_time)
    end_time = db.Column(db.DateTime, default=None)
    hostname = db.Column(db.String(100))
    tests = db.relationship('Test', backref=backref('session'), cascade='all, delete, delete-orphan')


class Test(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id', ondelete='CASCADE'), index=True)
    start_time = db.Column(db.DateTime, default=get_current_time)
    end_time = db.Column(db.DateTime, default=None)
    name = db.Column(db.String(256))

    @computed_field
    def duration(self):
        if self.end_time is None or self.start_time is None:
            return None
        return (self.end_time - self.start_time).total_seconds()
