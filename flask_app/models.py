from .app import app
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from flask import json

db = SQLAlchemy(app)

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

class Session(db.Model):
    #TODO: do we want to tight couple backslash and slash? id is id?
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.String)
    version = db.Column(db.String)
    environment = db.Column(db.String)
    status = db.Column(db.Enum('RUNNING', 'FINISHED', name='session_status'))
    start_time = db.Column(db.DateTime)
    finish_time = db.Column(db.DateTime)
    total_runtime = db.Column(db.Integer)
    passed_tests = db.Column(db.Integer)
    failed_tests = db.Column(db.Integer)
    error_tests = db.Column(db.Integer)
    session_metadata = db.Column(JSON)

    tests = db.relationship("Test", backref="session", lazy='dynamic')

    def __init__(self, session_id):
        self.session_id = session_id

    def __repr__(self):
        return '<Session %r>' % self.session_id

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'id': self.id,
           'session_id': self.session_id,
           #'modified_at': dump_datetime(self.modified_at)
           'user_id': self.user_id,
           'version': self.version
        }

class Test(db.Model):
    #TODO: do we want to tight couple backslash and slash? id is id?
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, unique=True)

    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    #session = db.relationship("Session", backref=db.backref('tests', order_by=id))

    status = db.Column(db.Enum('PASSED', 'FAILED', 'ERROR', name='test_status'))
    start_time = db.Column(db.DateTime)
    finish_time = db.Column(db.DateTime)
    total_runtime = db.Column(db.Integer)
    test_metadata = db.Column(JSON)

    def __init__(self, session_id, test_id):
        self.session_id = session_id
        self.test_id = test_id

    def __repr__(self):
        return '<Test %r>' % self.test_id

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'id': self.id,
           'test_id': self.test_id,
           'start_time': dump_datetime(self.start_time)
        }
