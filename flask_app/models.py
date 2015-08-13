import datetime

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import UserMixin, RoleMixin, current_user

from sqlalchemy.orm import backref
from sqlalchemy import UniqueConstraint

from .utils import statuses

from .utils import get_current_time
from .utils.rendering import rendered_field
from . import activity

from sqlalchemy.dialects.postgresql import JSON, JSONB


db = SQLAlchemy()


class TypenameMixin(object):

    @classmethod
    def get_typename(cls):
        return cls.__name__.lower()


class StatusPredicatesMixin(object):

    @property
    def skipped(self):
        return self.status == statuses.SKIPPED

    @property
    def interrupted(self):
        return self.status == statuses.INTERRUPTED

    @property
    def failed(self):
        return self.status == statuses.FAILURE

    @property
    def errored(self):
        return self.status == statuses.ERROR





test_error = db.Table('test_error',
                      db.Column('test_id',
                                db.Integer,
                                db.ForeignKey('test.id', ondelete='CASCADE')),
                      db.Column('error_id',
                                db.Integer,
                                db.ForeignKey('error.id', ondelete='CASCADE')))

session_error = db.Table('session_error',
                         db.Column('session_id',
                                   db.Integer,
                                   db.ForeignKey('session.id', ondelete='CASCADE')),
                         db.Column('error_id',
                                   db.Integer,
                                   db.ForeignKey('error.id', ondelete='CASCADE')))

test_comment = db.Table('test_comment',
                        db.Column('test_id',
                                  db.Integer,
                                  db.ForeignKey('test.id', ondelete='CASCADE')),
                        db.Column('comment_id',
                                  db.Integer,
                                  db.ForeignKey('comment.id', ondelete='CASCADE')))

session_comment = db.Table('session_comment',
                           db.Column('session_id',
                                     db.Integer,
                                     db.ForeignKey('session.id', ondelete='CASCADE')),
                           db.Column('comment_id',
                                     db.Integer,
                                     db.ForeignKey('comment.id', ondelete='CASCADE')))

session_subject = db.Table('session_subject',
                           db.Column('session_id',
                                     db.Integer,
                                     db.ForeignKey('session.id', ondelete='CASCADE')),
                           db.Column('subject_id',
                                     db.Integer,
                                     db.ForeignKey('subject_instance.id', ondelete='CASCADE')))



class Session(db.Model, TypenameMixin, StatusPredicatesMixin):

    id = db.Column(db.Integer, primary_key=True)
    logical_id = db.Column(db.String(256), index=True)
    start_time = db.Column(db.Float, default=get_current_time)
    end_time = db.Column(db.Float, default=None)
    hostname = db.Column(db.String(100))


    archived = db.Column(db.Boolean(), server_default="false", nullable=False) # no sense of indexing this since it's usually False
    investigated = db.Column(db.Boolean(), server_default='false')

    edited_status = db.Column(db.String(256), index=True)
    tests = db.relationship(
        'Test', backref=backref('session'), cascade='all, delete, delete-orphan')
    errors = db.relationship(
        'Error', secondary=session_error, backref=backref('session', lazy='dynamic'))
    comments = db.relationship(
        'Comment', secondary=session_comment, backref=backref('session', lazy='dynamic'))
    metadata_items = db.relationship(
        'SessionMetadata', backref='session', lazy='dynamic', cascade='all, delete, delete-orphan')

    subject_instances = db.relationship(
        'SubjectInstance', secondary=session_subject, backref=backref('sessions', lazy='joined'), lazy=False)

    # test counts
    total_num_tests = db.Column(db.Integer, default=None)
    num_failed_tests = db.Column(db.Integer, default=0)
    num_error_tests = db.Column(db.Integer, default=0)
    num_skipped_tests = db.Column(db.Integer, default=0)
    num_finished_tests = db.Column(db.Integer, default=0)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), index=True, nullable=False)
    user = db.relationship('User', lazy='joined')

    # status
    num_errors = db.Column(db.Integer, default=0)
    num_failures = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), nullable=False, default=statuses.STARTED, index=True)

    # rendered extras
    @rendered_field
    def user_email(self):
        return self.user.email

    @rendered_field
    def subjects(self):
        return [
            {'name': s.subject.name, 'product': s.revision.product_version.product.name,
             'version': s.revision.product_version.version, 'revision': s.revision.revision}
            for s in self.subject_instances]


class SubjectInstance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), index=True, nullable=False)
    subject = db.relationship('Subject', lazy='joined')
    revision_id = db.Column(db.Integer, db.ForeignKey('product_revision.id'), index=True)
    revision = db.relationship('ProductRevision', lazy='joined')


class Subject(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)


class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)

    versions = db.relationship(
        'ProductVersion', backref=backref('product'), cascade='all, delete, delete-orphan')


class ProductVersion(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(256))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint('product_id', 'version'),
    )

    revisions = db.relationship(
        'ProductRevision', backref=backref('product_version'), cascade='all, delete, delete-orphan')


class ProductRevision(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    product_version_id = db.Column(db.Integer, db.ForeignKey('product_version.id'), nullable=False, index=True)
    revision = db.Column(db.String(256))

    __table_args__ = (
        UniqueConstraint('product_version_id', 'revision'),
    )


class TestInformation(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(1024), nullable=True, index=True)
    class_name = db.Column(db.String(256), nullable=True, index=True)
    name = db.Column(db.String(256), nullable=False, index=True)


class Test(db.Model, TypenameMixin, StatusPredicatesMixin):

    id = db.Column(db.Integer, primary_key=True)

    test_info_id = db.Column(db.Integer, db.ForeignKey('test_information.id', ondelete='CASCADE'), index=True)
    test_info = db.relationship('TestInformation', lazy='joined')

    session_id = db.Column(
        db.Integer, db.ForeignKey('session.id', ondelete='CASCADE'), index=True)
    logical_id = db.Column(db.String(256), index=True)
    start_time = db.Column(db.Float, default=get_current_time)
    end_time = db.Column(db.Float, default=None)
    num_errors = db.Column(db.Integer, default=0)
    num_failures = db.Column(db.Integer, default=0)
    edited_status = db.Column(db.String(256), index=True)
    errors = db.relationship(
        'Error', secondary=test_error, backref=backref('test', lazy='dynamic'))
    comments = db.relationship(
        'Comment', secondary=test_comment, backref=backref('test', lazy='dynamic'))

    status = db.Column(db.String(20), nullable=False, default=statuses.STARTED, index=True)

    @rendered_field
    def duration(self):
        if self.end_time is None or self.start_time is None:
            return None
        return self.end_time - self.start_time

    @rendered_field
    def info(self):
        return {attr: getattr(self.test_info, attr)
                for attr in ('file_name', 'class_name', 'name')}


_METADATA_KEY_TYPE = db.String(1024)


class TestMetadata(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(
        db.Integer, db.ForeignKey('test.id', ondelete='CASCADE'), index=True)
    key = db.Column(_METADATA_KEY_TYPE, nullable=False)
    metadata_item = db.Column(JSONB)


class SessionMetadata(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(
        db.Integer, db.ForeignKey('session.id', ondelete='CASCADE'), index=True)
    key = db.Column(_METADATA_KEY_TYPE, nullable=False)
    metadata_item = db.Column(JSONB)


class Error(db.Model, TypenameMixin):

    id = db.Column(db.Integer, primary_key=True)
    traceback = db.Column(JSON)
    exception_type = db.Column(db.String(256), index=True)
    message = db.Column(db.String(256), index=True)
    timestamp = db.Column(db.Float, default=get_current_time)
    is_failure = db.Column(db.Boolean, default=False)


roles_users = db.Table('roles_users',
                       db.Column(
                           'user_id', db.Integer(), db.ForeignKey('user.id')),
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
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User')
    token = db.Column(db.String(255), unique=True, index=True)


class Comment(db.Model, TypenameMixin):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False, index=True)
    user = db.relationship('User')
    comment = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.Float, default=get_current_time)
    deleted = db.Column(db.Boolean, server_default="false")

    @rendered_field
    def user_email(self):
        return self.user.email

    @rendered_field
    def can(self):
        is_mine = self.user_id == current_user.id
        return {
            'delete': is_mine,
            'edit': is_mine,
        }


class Activity(db.Model, TypenameMixin):

    id = db.Column(db.Integer, primary_key=True)

    action = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.Float, default=get_current_time)

    test_id = db.Column(db.Integer, db.ForeignKey('test.id', ondelete='CASCADE'), nullable=True, index=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id', ondelete='CASCADE'), nullable=True, index=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True, index=True)
    user = db.relationship('User', lazy='joined')

    @rendered_field
    def what(self):
        if self.test_id is not None:
            return 'test'
        if self.session_id is not None:
            return 'session'
        return None

    @rendered_field
    def user_email(self):
        return self.user.email

    @rendered_field
    def action_string(self):
        return activity.get_action_string(self.action)

    def __repr__(self):
        return '<{} {} {}>'.format(self.user_id, self.action_string(), self.what())
