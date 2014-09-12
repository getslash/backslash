import datetime

from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy.orm import backref

from .app import app
from .utils import get_current_time

db = SQLAlchemy(app)

### Add models here


class Session(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    logical_id = db.Column(db.Integer, unique=True)
    start_time = db.Column(db.DateTime, default=get_current_time)
    end_time = db.Column(db.DateTime, default=None)
    hostname = db.Column(db.String(100))
    product_name = db.Column(db.String(256))
    product_version = db.Column(db.String(256))
    product_revision = db.Column(db.String(256))
    tests = db.relationship('Test', backref=backref('session'), cascade='all, delete, delete-orphan')

    def __init__(self, logical_id, hostname=None,
                 product_name=None, product_version=None, product_revision=None):
        self.logical_id = logical_id
        self.hostname = hostname
        self.product_name = product_name
        self.product_version = product_version
        self.product_revision = product_revision


class Test(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id', ondelete='CASCADE'), index=True)
    logical_id = db.Column(db.Integer, unique=True)
    start_time = db.Column(db.DateTime, default=get_current_time)
    end_time = db.Column(db.DateTime, default=None)
    name = db.Column(db.String(256))

    def __init__(self, session_id, logical_id, name):
        self.session_id = session_id  # this is not the logical_id - the real ID is the foreign key
        self.logical_id = logical_id
        self.name = name

