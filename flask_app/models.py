import datetime

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import UserMixin, RoleMixin

from sqlalchemy.orm import backref

from .utils import get_current_time
from .utils.rendering import computed_field

from sqlalchemy.dialects.postgresql import JSON, JSONB


db = SQLAlchemy()


test_error = db.Table('test_error',
                      db.Column('test_id',
                                db.Integer,
                                db.ForeignKey('test.id')),
                      db.Column('error_id',
                                db.Integer,
                                db.ForeignKey('error.id')))

session_error = db.Table('session_error',
                         db.Column('session_id',
                                   db.Integer,
                                   db.ForeignKey('session.id')),
                         db.Column('error_id',
                                   db.Integer,
                                   db.ForeignKey('error.id')))


class TypenameMixin(object):

    @classmethod
    def get_typename(cls):
        return cls.__name__.lower()


class Session(db.Model, TypenameMixin):

    id = db.Column(db.Integer, primary_key=True)
    logical_id = db.Column(db.String(256), index=True)
    start_time = db.Column(db.Float, default=get_current_time)
    end_time = db.Column(db.Float, default=None)
    hostname = db.Column(db.String(100))
    product_name = db.Column(db.String(256), index=True)
    product_version = db.Column(db.String(256), index=True)
    product_revision = db.Column(db.String(256), index=True)

    edited_status = db.Column(db.String(256), index=True)
    tests = db.relationship('Test', backref=backref('session'), cascade='all, delete, delete-orphan')
    errors = db.relationship('Error', secondary=session_error, backref=backref('session', lazy='dynamic'))
    metadata_items = db.relationship('SessionMetadata', backref='session', lazy='dynamic', cascade='all, delete, delete-orphan')


    # test counts
    total_num_tests = db.Column(db.Integer, default=None)
    num_failed_tests = db.Column(db.Integer, default=0)
    num_error_tests = db.Column(db.Integer, default=0)
    num_skipped_tests = db.Column(db.Integer, default=0)
    num_finished_tests = db.Column(db.Integer, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
    user = db.relationship('User', lazy='joined')

    @computed_field
    def status(self):
        if self.edited_status:
            return self.edited_status
        if len(self.errors) > 0:
            return 'FAILURE'
        if self.end_time is None:
            return 'RUNNING'
        else:
            for test in self.tests:
                if test.status() == 'FAILURE' or test.status() == 'ERROR':
                    return 'FAILURE'
            return 'SUCCESS'


class Test(db.Model, TypenameMixin):

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id', ondelete='CASCADE'), index=True)
    logical_id = db.Column(db.String(256), index=True)
    start_time = db.Column(db.Float, default=get_current_time)
    end_time = db.Column(db.Float, default=None)
    name = db.Column(db.String(256), index=True)
    skipped = db.Column(db.Boolean, default=False)
    interrupted = db.Column(db.Boolean, default=False)
    num_errors = db.Column(db.Integer, default=0)
    num_failures = db.Column(db.Integer, default=0)
    edited_status = db.Column(db.String(256), index=True)
    test_conclusion = db.Column(db.String(256), index=True)
    errors = db.relationship('Error', secondary=test_error, backref=backref('test', lazy='dynamic'))

    @computed_field
    def duration(self):
        if self.end_time is None or self.start_time is None:
            return None
        return self.end_time - self.start_time

    @computed_field
    def status(self):
        if self.edited_status:
            return self.edited_status
        if self.interrupted:
            return 'INTERRUPTED'
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

_METADATA_KEY_TYPE = db.String(1024)

class TestMetadata(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id', ondelete='CASCADE'), index=True)
    key = db.Column(_METADATA_KEY_TYPE, nullable=False)
    metadata_item = db.Column(JSONB)


class SessionMetadata(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id', ondelete='CASCADE'), index=True)
    key = db.Column(_METADATA_KEY_TYPE, nullable=False)
    metadata_item = db.Column(JSONB)


class Error(db.Model, TypenameMixin):

    id = db.Column(db.Integer, primary_key=True)
    traceback = db.Column(JSON)
    exception_type = db.Column(db.String(256), index=True)
    exception = db.Column(db.String(256), index=True)
    timestamp = db.Column(db.Float, default=get_current_time)

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin, TypenameMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, lazy='joined',
                            backref=db.backref('users', lazy='dynamic'))


class RunToken(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User')
    token = db.Column(db.String(255), unique=True, index=True)
