import datetime

from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy.orm import backref

from .app import app

db = SQLAlchemy(app)

### Add models here

class Session(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    end_time = db.Column(db.DateTime, default=None)
    hostname = db.Column(db.String(100))
    tests = db.relationship('Test', backref=backref('session'), cascade='all, delete, delete-orphan')


class Test(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id', ondelete='CASCADE'), index=True)
    name = db.Column(db.String(256))
