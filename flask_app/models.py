from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import UserMixin, RoleMixin, current_user

from sqlalchemy.orm import backref
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import and_, select, func

from .utils import statuses

from .utils import get_current_time
from .utils.rendering import rendered_field, render_api_object, rendered_only_on_single
from . import activity
from .capabilities import CAPABILITIES

from sqlalchemy import Index
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import JSON, JSONB


db = SQLAlchemy()


class TypenameMixin(object):

    @classmethod
    def get_typename(cls):
        return cls.__name__.lower()


class HasRelatedMixin(object):

    @rendered_only_on_single
    def related(self):
        return [{'name': obj.name, 'type': obj.type} for obj in self.related_entities]


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



session_subject = db.Table('session_subject',
                           db.Column('session_id',
                                     db.Integer,
                                     db.ForeignKey('session.id', ondelete='CASCADE')),
                           db.Column('subject_id',
                                     db.Integer,
                                     db.ForeignKey('subject_instance.id', ondelete='CASCADE')))



class Session(db.Model, TypenameMixin, StatusPredicatesMixin, HasRelatedMixin):

    id = db.Column(db.Integer, primary_key=True)
    logical_id = db.Column(db.String(256), index=True)
    start_time = db.Column(db.Float, default=get_current_time)
    end_time = db.Column(db.Float, default=None, index=True)
    hostname = db.Column(db.String(100))

    in_pdb = db.Column(db.Boolean, server_default='FALSE')

    infrastructure = db.Column(db.String(50), default=None)

    archived = db.Column(db.Boolean(), server_default="false", nullable=False) # no sense of indexing this since it's usually False
    investigated = db.Column(db.Boolean(), server_default='false')

    tests = db.relationship(
        'Test', backref=backref('session', lazy='joined'), cascade='all, delete, delete-orphan')
    errors = db.relationship(
        'Error', backref=backref('session', lazy='joined'))
    comments = db.relationship(
        'Comment', primaryjoin='Comment.session_id==Session.id')
    metadata_items = db.relationship(
        'SessionMetadata', lazy='dynamic', cascade='all, delete, delete-orphan')

    subject_instances = db.relationship(
        'SubjectInstance', secondary=session_subject, backref=backref('sessions', lazy='subquery'), lazy='subquery')

    # test counts
    total_num_tests = db.Column(db.Integer, default=None)
    num_failed_tests = db.Column(db.Integer, default=0)
    num_error_tests = db.Column(db.Integer, default=0)
    num_skipped_tests = db.Column(db.Integer, default=0)
    num_finished_tests = db.Column(db.Integer, default=0)

    num_warnings = db.Column(db.Integer, nullable=False, server_default="0")
    num_test_warnings = db.Column(db.Integer, nullable=False, server_default="0")

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), index=True, nullable=False)
    user = db.relationship('User', lazy='joined', foreign_keys=user_id)
    real_user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
    real_user = db.relationship('User', lazy='joined', foreign_keys=real_user_id)


    # status
    num_errors = db.Column(db.Integer, default=0)
    num_failures = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), nullable=False, default=statuses.STARTED, index=True)

    # keepalive
    keepalive_interval = db.Column(db.Integer, nullable=True, default=None)
    next_keepalive = db.Column(db.Float, nullable=True, default=None, index=True)

    # activity
    num_comments = db.Column(db.Integer, default=0)

    __table_args__ = (
        Index('ix_session_start_time', start_time.desc()),
    )



    @rendered_field
    def is_abandoned(self):
        if self.next_keepalive is None:
            return False
        if self.next_keepalive > get_current_time():
            return False
        return self.end_time is None

    # rendered extras
    related_entities = db.relationship('RelatedEntity')

    @rendered_field
    def user_email(self):
        return self.user.email

    @rendered_field
    def user_display_name(self):
        return self.user.display_name()


    @rendered_field
    def real_email(self):
        user = self.real_user
        if user is None:
            return None
        return user.email

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

    @rendered_field
    def name(self):
        return self.subject.name


class RelatedEntity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(256), nullable=False)
    name = db.Column(db.Text(), nullable=False)
    test_id = db.Column(db.ForeignKey('test.id', ondelete='CASCADE'), nullable=True, index=True)
    session_id = db.Column(db.ForeignKey('session.id', ondelete='CASCADE'), nullable=True, index=True)


class Subject(db.Model, TypenameMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, index=True, unique=True)
    last_activity = db.Column(db.Float(), index=True)


class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)

    versions = db.relationship(
        'ProductVersion', backref=backref('product', lazy='joined'), cascade='all, delete, delete-orphan')


class ProductVersion(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(256))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint('product_id', 'version'),
    )

    revisions = db.relationship(
        'ProductRevision', cascade='all, delete, delete-orphan')


class ProductRevision(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    product_version_id = db.Column(db.Integer, db.ForeignKey('product_version.id'), nullable=False, index=True)
    product_version = db.relationship(ProductVersion, lazy='joined')
    revision = db.Column(db.String(256))

    __table_args__ = (
        UniqueConstraint('product_version_id', 'revision'),
    )


class TestInformation(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(1024), nullable=True, index=True)
    class_name = db.Column(db.String(256), nullable=True, index=True)
    name = db.Column(db.String(256), nullable=False, index=True)

    @classmethod
    def get_typename(cls):
        return 'test_info'



class TestVariation(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    variation = db.Column(JSONB)


class Test(db.Model, TypenameMixin, StatusPredicatesMixin, HasRelatedMixin):

    id = db.Column(db.Integer, primary_key=True)

    test_info_id = db.Column(db.Integer, db.ForeignKey('test_information.id', ondelete='CASCADE'), index=True)
    test_info = db.relationship('TestInformation', lazy='joined')

    test_variation_id = db.Column(db.Integer, db.ForeignKey('test_variation.id', ondelete='CASCADE'), index=True)
    test_variation = db.relationship('TestVariation', lazy='joined')

    @rendered_field
    def variation(self):
        v = self.test_variation
        if v is None:
            return None
        return v.variation

    scm = db.Column(db.String(5), default=None)
    scm_dirty = db.Column(db.Boolean, server_default='false')
    scm_revision = db.Column(db.String(40), default=None)
    file_hash = db.Column(db.String(40), default=None)

    session_id = db.Column(
        db.Integer, db.ForeignKey('session.id', ondelete='CASCADE'), index=True)

    logical_id = db.Column(db.String(256), index=True)
    start_time = db.Column(db.Float, default=get_current_time)
    end_time = db.Column(db.Float, default=None)

    errors = db.relationship('Error')
    comments = db.relationship('Comment', primaryjoin='Comment.test_id==Test.id')

    first_error_obj = db.relationship(lambda: Error,
                                  primaryjoin=lambda: and_(
                                      Test.id == Error.test_id,
                                      Error.timestamp == select([func.min(Error.timestamp)]).
                                      where(Error.test_id==Test.id).
                                      correlate(Test.__table__)
                                  ),
                                  uselist=False,
                                  lazy='joined'
                              )

    related_entities = db.relationship('RelatedEntity')

    is_interactive = db.Column(db.Boolean, server_default='FALSE')

    status = db.Column(db.String(20), nullable=False, default=statuses.STARTED, index=True)

    skip_reason = db.Column(db.Text(), nullable=True)

    num_errors = db.Column(db.Integer, default=0)
    num_failures = db.Column(db.Integer, default=0)
    num_comments = db.Column(db.Integer, default=0)
    num_warnings = db.Column(db.Integer, nullable=False, server_default="0")

    __table_args__ = (
        Index('ix_test_start_time', start_time.desc()),
    )

    @rendered_field
    def duration(self):
        if self.end_time is None or self.start_time is None:
            return None
        return self.end_time - self.start_time

    @rendered_field
    def first_error(self):
        if self.first_error_obj is None:
            return None
        return render_api_object(self.first_error_obj, only_fields={'message', 'exception_type'})


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
    session = db.relationship('Session', lazy='joined')
    key = db.Column(_METADATA_KEY_TYPE, nullable=False)
    metadata_item = db.Column(JSONB)


class Error(db.Model, TypenameMixin):

    id = db.Column(db.Integer, primary_key=True)
    traceback = db.Column(JSON)
    exception_type = db.Column(db.String(256), index=True)
    message = db.Column(db.Text())
    timestamp = db.Column(db.Float, default=get_current_time)
    is_failure = db.Column(db.Boolean, default=False)
    test_id = db.Column(db.ForeignKey('test.id', ondelete='CASCADE'), nullable=True, index=True)
    session_id = db.Column(db.ForeignKey('session.id', ondelete='CASCADE'), nullable=True, index=True)


class Warning(db.Model, TypenameMixin):

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.ForeignKey('test.id', ondelete='CASCADE'), nullable=True, index=True)
    session_id = db.Column(db.ForeignKey('session.id', ondelete='CASCADE'), nullable=True, index=True)
    message = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String(2048), nullable=True)
    lineno = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.Float, nullable=False)



roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin, TypenameMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, lazy='joined')
    run_tokens = db.relationship('RunToken', lazy='dynamic')

    last_activity = db.Column(db.Float())

    @rendered_field
    def full_name(self):
        if self.first_name is None or self.last_name is None:
            return None
        return self.first_name + " " + self.last_name

    @rendered_field
    def display_name(self):
        fullname = self.full_name()
        if fullname is None:
            return self.email.split('@')[0]
        return fullname

    @rendered_field
    def user_roles(self):
        return [{'name': role.name} for role in self.roles]

    @rendered_field
    def capabilities(self):
        return {cap_name: True for cap_name, cap in CAPABILITIES.items() if cap.enabled_for(self)}


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
    user = db.relationship('User', foreign_keys=user_id)
    comment = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.Float, default=get_current_time)
    deleted = db.Column(db.Boolean, server_default="false")
    session_id = db.Column(db.ForeignKey(Session.id, ondelete='CASCADE'), nullable=True, index=True)
    test_id = db.Column(db.ForeignKey(Test.id, ondelete='CASCADE'), nullable=True, index=True)

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


class Stat(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    timestamp = db.Column(db.Float, default=get_current_time, index=True)

    __table_args__ = (
        Index('ix_stat_timestamp', timestamp.desc()),
    )

    ### statistics
    stat_db_size = db.Column(db.BIGINT, server_default="0")
    stat_num_new_sessions = db.Column(db.Integer, server_default="0")
    stat_system_load_avg = db.Column(db.Float, server_default="0")
