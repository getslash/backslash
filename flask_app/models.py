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
    logical_id = db.Column(db.String(256))
    start_time = db.Column(db.Float, default=get_current_time)
    end_time = db.Column(db.Float, default=None)
    hostname = db.Column(db.String(100))
    product_name = db.Column(db.String(256), index=True)
    product_version = db.Column(db.String(256), index=True)
    product_revision = db.Column(db.String(256), index=True)
    tests = db.relationship('Test', backref=backref('session'), cascade='all, delete, delete-orphan')

    @computed_field
    def status(self):
        if self.end_time is None:
            return 'RUNNING'
        else:
            for test in self.tests:
                if test.status() == 'FAILURE' or test.status() == 'ERROR':
                    return 'FAILURE'
            return 'SUCCESS'


class Test(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id', ondelete='CASCADE'), index=True)
    logical_id = db.Column(db.String(256))
    start_time = db.Column(db.Float, default=get_current_time)
    end_time = db.Column(db.Float, default=None)
    name = db.Column(db.String(256))
    skipped = db.Column(db.Boolean, default=False)
    num_errors = db.Column(db.Integer, default=0)
    num_failures = db.Column(db.Integer, default=0)

    @computed_field
    def duration(self):
        if self.end_time is None or self.start_time is None:
            return None
        return self.end_time - self.start_time

    @computed_field
    def status(self):
        if self.end_time is None:
            return 'RUNNING'
        else:
            if self.skipped:
                return 'SKIPPED'
            if self.num_failures > 0:
                return 'FAILURE'
            elif self.num_errors > 0:
                return 'ERROR'
        return 'SUCCESS'
