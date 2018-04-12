from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin, current_user
import flux

from sqlalchemy.orm import backref
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import and_, select, func

from .utils import statuses

from .utils import get_current_time
from .utils.rendering import rendered_field, render_api_object
from .capabilities import CAPABILITIES

from psycopg2.extras import DateTimeTZRange
from sqlalchemy import Index, CheckConstraint
from sqlalchemy.dialects.postgresql import JSON, JSONB, TSTZRANGE


db = SQLAlchemy()


class TypenameMixin:

    @classmethod
    def get_typename(cls):
        return cls.__name__.lower()


class UserDetailsMixin:

    @rendered_field
    def user_email(self):
        return self.user.email

    @rendered_field
    def user_display_name(self):
        return self.user.display_name()


class HasSubjectsMixin:

    @rendered_field
    def subjects(self):
        return [
            {'name': s.subject.name, 'product': s.revision.product_version.product.name,
             'version': s.revision.product_version.version, 'revision': s.revision.revision}
            for s in self.subject_instances]



class StatusPredicatesMixin:

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


class TimespanMixin:

    timespan = db.Column(TSTZRANGE, nullable=True)

    def mark_started(self):
        self.start_time = get_current_time()
        end_time = None
        session_id = getattr(self, "session_id", None)
        if session_id is not None:
            session = Session.query.get(session_id)
            if session.keepalive_interval is not None:
                end_time = datetime.fromtimestamp(self.start_time + session.keepalive_interval)
        self.timespan = DateTimeTZRange(datetime.fromtimestamp(self.start_time), end_time)

    def extend_timespan_to(self, timestamp):
        if self.start_time is None:
            return
        start_time = datetime.fromtimestamp(self.start_time)
        end_time = max(start_time, datetime.fromtimestamp(timestamp))
        self.timespan = DateTimeTZRange(start_time, end_time)

    def mark_ended(self):
        self.mark_ended_at(get_current_time())

    def mark_ended_at(self, timestamp):
        self.end_time = timestamp
        self.extend_timespan_to(timestamp)


subject_seq = db.Sequence('subject_seq')

session_subject = db.Table('session_subject',
                           db.Column('ordinal', db.Integer, subject_seq, server_default=subject_seq.next_value()),
                           db.Column('session_id',
                                     db.Integer,
                                     db.ForeignKey('session.id', ondelete='CASCADE')),
                           db.Index('ix_session_subject_session_id', 'session_id'),
                           db.Column('subject_id',
                                     db.Integer,
                                     db.ForeignKey('subject_instance.id', ondelete='CASCADE')))



class Session(db.Model, TypenameMixin, StatusPredicatesMixin, HasSubjectsMixin, UserDetailsMixin, TimespanMixin):

    id = db.Column(db.Integer, primary_key=True)
    logical_id = db.Column(db.String(256), unique=True, index=True)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now, index=True, nullable=True)

    parent_logical_id = db.Column(db.String(256), db.ForeignKey('session.logical_id', ondelete='CASCADE'), default=None, index=True)
    children = db.relationship('Session', backref=backref('parent', remote_side=[logical_id]))
    is_parent_session = db.Column(db.Boolean, server_default='FALSE')
    child_id = db.Column(db.String(20), default=None)

    start_time = db.Column(db.Float, default=get_current_time)
    end_time = db.Column(db.Float, default=None, index=True)
    hostname = db.Column(db.String(100))

    in_pdb = db.Column(db.Boolean, server_default='FALSE')

    infrastructure = db.Column(db.String(50), default=None)

    tests = db.relationship(
        'Test', backref=backref('session', lazy='joined'), cascade='all, delete, delete-orphan')
    errors = db.relationship(
        'Error', backref=backref('session', lazy='joined'))
    comments = db.relationship(
        'Comment', primaryjoin='Comment.session_id==Session.id')
    metadata_items = db.relationship(
        'SessionMetadata', lazy='dynamic', cascade='all, delete, delete-orphan')

    subject_instances = db.relationship(
        'SubjectInstance', secondary=session_subject, backref=backref('sessions', lazy='dynamic'), lazy='joined', order_by=session_subject.c.ordinal)

    labels = db.relationship('Label', secondary='session_label', lazy='joined')

    # test counts
    total_num_tests = db.Column(db.Integer, default=None)
    num_failed_tests = db.Column(db.Integer, default=0)
    num_error_tests = db.Column(db.Integer, default=0)
    num_skipped_tests = db.Column(db.Integer, default=0)
    num_finished_tests = db.Column(db.Integer, default=0)
    num_interruptions = db.Column(db.Integer, default=0)
    num_interrupted_tests = db.Column(db.Integer, server_default="0")
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
    status = db.Column(db.String(20), nullable=False, default=statuses.STARTED)

    # keepalive
    keepalive_interval = db.Column(db.Integer, nullable=True, default=None)
    next_keepalive = db.Column(db.Float, nullable=True, default=None, index=True)

    # activity
    num_comments = db.Column(db.Integer, default=0)

    has_fatal_errors = db.Column(db.Boolean, default=False)

    delete_at = db.Column(db.Float, nullable=True)
    ttl_seconds = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        Index('ix_session_start_time', start_time.desc()),
        Index('ix_session_status_lower', func.lower(status)),
        Index('ix_session_start_time_status_lower', start_time.desc(), func.lower(status)),
        Index('ix_session_timespan', 'timespan', postgresql_using='gist'),
        Index('ix_session_delete_at', delete_at, postgresql_where=(delete_at != None)),
        Index('ix_session_updated_at', updated_at.asc(), postgresql_where=(updated_at != None)),
    )


    last_comment_obj = db.relationship(lambda: Comment,
                                  primaryjoin=lambda: and_(
                                      Session.id == Comment.session_id, # pylint: disable=undefined-variable
                                      Comment.timestamp == select([func.max(Comment.timestamp)]).
                                      where(Comment.session_id == Session.id).
                                      correlate(Session.__table__)
                                  ),
                                  uselist=False,
                                  lazy='joined'
                              )

    @rendered_field
    def last_comment(self):
        comment = self.last_comment_obj
        if comment is None:
            return None

        return {'comment': comment.comment, 'user_email': comment.user.email}


    @rendered_field
    def is_abandoned(self):
        if self.next_keepalive is None:
            return False
        if self.next_keepalive > get_current_time():
            return False
        return self.end_time is None

    # rendered extras
    related_entities = db.relationship('Entity', secondary='session_entity')

    @rendered_field
    def real_email(self):
        user = self.real_user
        if user is None:
            return None
        return user.email

    @rendered_field(name='labels')
    def label_names(self):
        return [l.name for l in self.labels]


    def update_keepalive(self):
        if self.keepalive_interval is not None:
            next_keepalive = flux.current_timeline.time() + self.keepalive_interval
            self.next_keepalive = next_keepalive
            self.extend_timespan_to(next_keepalive)
            if self.ttl_seconds is not None:
                self.delete_at = self.next_keepalive + self.ttl_seconds

    def notify_subject_activity(self):
        for subject_instance in self.subject_instances:
            subject_instance.subject.last_activity = max(subject_instance.subject.last_activity or 0, flux.current_timeline.time())


class SubjectInstance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), index=True, nullable=False)
    subject = db.relationship('Subject', lazy='joined')
    revision_id = db.Column(db.Integer, db.ForeignKey('product_revision.id'), index=True)
    revision = db.relationship('ProductRevision', lazy='joined')

    @rendered_field
    def name(self):
        return self.subject.name


class Entity(db.Model, TypenameMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    type = db.Column(db.String(256), nullable=False)

    @rendered_field
    def entity_type(self):
        return self.type

    __table_args__ = (
        Index('ix_entity', name, type, unique=True),
    )



session_entity = db.Table('session_entity',
                           db.Column('session_id',
                                     db.Integer,
                                     db.ForeignKey('session.id', ondelete='CASCADE'), index=True),
                           db.Column('entity_id',
                                     db.Integer,
                                     db.ForeignKey('entity.id', ondelete='CASCADE'), index=True),
                           db.Index('ix_session_entity_session_id_entity_id', 'session_id', 'entity_id'),
)

test_entity = db.Table('test_entity',
                           db.Column('test_id',
                                     db.Integer,
                                     db.ForeignKey('test.id', ondelete='CASCADE'), index=True),
                           db.Column('entity_id',
                                     db.Integer,
                                     db.ForeignKey('entity.id', ondelete='CASCADE'), index=True),
                           db.Index('ix_test_entity_test_id_entity_id', 'test_id', 'entity_id'),
)



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
        return 'case'



class TestVariation(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    variation = db.Column(JSONB)


class Test(db.Model, TypenameMixin, StatusPredicatesMixin, HasSubjectsMixin, UserDetailsMixin, TimespanMixin):

    id = db.Column(db.Integer, primary_key=True)

    test_index = db.Column(db.Integer)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now, index=True, nullable=True)
    test_info_id = db.Column(db.Integer, db.ForeignKey('test_information.id', ondelete='CASCADE'), index=True)
    test_info = db.relationship('TestInformation', lazy='joined')

    test_variation_id = db.Column(db.Integer, db.ForeignKey('test_variation.id', ondelete='CASCADE'), index=True)
    test_variation = db.relationship('TestVariation', lazy='joined')

    subject_instances = db.relationship(
        'SubjectInstance', secondary=session_subject, primaryjoin='Test.session_id==session_subject.c.session_id', lazy='joined', order_by=session_subject.c.ordinal)

    user = db.relationship('User', secondary=Session.__table__, primaryjoin='Test.session_id==Session.id', secondaryjoin='Session.user_id==User.id', lazy='joined', uselist=False)

    metadatas = db.relationship('TestMetadata', lazy='dynamic')

    parameters = db.Column(JSONB)

    @rendered_field
    def variation(self):
        v = self.test_variation
        if v is None:
            return None
        return v.variation

    @rendered_field
    def session_display_id(self):
        return self.session.logical_id or self.session.id

    @rendered_field
    def is_session_abandoned(self):
        return self.session.is_abandoned()

    scm = db.Column(db.String(5), default=None)
    scm_dirty = db.Column(db.Boolean, server_default='false')
    scm_revision = db.Column(db.String(40), default=None)
    scm_local_branch = db.Column(db.String(256), default=None, nullable=True)
    scm_remote_branch = db.Column(db.String(256), default=None, nullable=True)
    file_hash = db.Column(db.String(40), default=None)

    session_id = db.Column(
        db.Integer, db.ForeignKey('session.id', ondelete='CASCADE'), index=True)

    logical_id = db.Column(db.String(256), index=True, unique=True)
    start_time = db.Column(db.Float, default=None, index=True)
    end_time = db.Column(db.Float, default=None, index=True)

    errors = db.relationship('Error')
    comments = db.relationship('Comment', primaryjoin='Comment.test_id==Test.id')

    first_error_obj = db.relationship(lambda: Error,
                                  primaryjoin=lambda: and_(
                                      Test.id == Error.test_id, # pylint: disable=undefined-variable
                                      Error.timestamp == select([func.min(Error.timestamp)]).
                                      where(Error.test_id == Test.id).
                                      correlate(Test.__table__)
                                  ),
                                  uselist=False,
                                  lazy='joined'
                              )

    @rendered_field
    def first_error(self):
        if self.first_error_obj is None:
            return None
        return render_api_object(self.first_error_obj, only_fields={'message', 'exception_type'})

    @rendered_field
    def first_error_id(self):
        if self.first_error_obj is None:
            return None
        return self.first_error_obj.id

    last_comment_obj = db.relationship(lambda: Comment,
                                  primaryjoin=lambda: and_(
                                      Test.id == Comment.test_id,
                                      Comment.timestamp == select([func.max(Comment.timestamp)]).
                                      where(Comment.test_id == Test.id).
                                      correlate(Test.__table__)
                                  ),
                                  uselist=False,
                                  lazy='joined'
                              )


    @rendered_field
    def last_comment(self):
        comment = self.last_comment_obj
        if comment is None:
            return None

        return {'comment': comment.comment, 'user_email': comment.user.email}


    related_entities = db.relationship('Entity', secondary='test_entity')

    is_interactive = db.Column(db.Boolean, server_default='FALSE')

    status = db.Column(db.String(20), nullable=False, default=statuses.STARTED)
    status_description = db.Column(db.String(1024), nullable=True)

    skip_reason = db.Column(db.Text(), nullable=True)

    num_errors = db.Column(db.Integer, default=0)
    num_failures = db.Column(db.Integer, default=0)
    num_comments = db.Column(db.Integer, default=0)
    num_warnings = db.Column(db.Integer, nullable=False, server_default="0")
    num_interruptions = db.Column(db.Integer, default=0)

    __table_args__ = (
        Index('ix_test_start_time', start_time.desc()),
        Index('ix_test_session_id_start_time', session_id, start_time),
        Index('ix_test_status_lower_start_time', func.lower(status), start_time.desc()),
        Index('ix_test_start_time_status_lower', start_time.desc(), func.lower(status)),
        Index('ix_test_test_info_id_start_time', test_info_id, start_time.desc()),
        Index('ix_test_timespan', 'timespan', postgresql_using='gist'),
        Index('ix_test_updated_at', updated_at.asc(), postgresql_where=(updated_at != None)),
    )

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
    session = db.relationship('Session', lazy='joined')
    key = db.Column(_METADATA_KEY_TYPE, nullable=False)
    metadata_item = db.Column(JSONB)


class Error(db.Model, TypenameMixin):

    id = db.Column(db.Integer, primary_key=True)
    traceback = db.Column(JSON)
    traceback_url = db.Column(db.String(2048))
    exception_type = db.Column(db.String(256), index=True)
    message = db.Column(db.Text())
    timestamp = db.Column(db.Float, default=get_current_time)
    is_failure = db.Column(db.Boolean, default=False)
    is_interruption = db.Column(db.Boolean, default=False)
    test_id = db.Column(db.ForeignKey('test.id', ondelete='CASCADE'), nullable=True, index=True)
    session_id = db.Column(db.ForeignKey('session.id', ondelete='CASCADE'), nullable=True, index=True)

    __table_args__ = (
        Index('ix_error_timestamp', timestamp),
    )



class Warning(db.Model, TypenameMixin):

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.ForeignKey('test.id', ondelete='CASCADE'), nullable=True, index=True)
    session_id = db.Column(db.ForeignKey('session.id', ondelete='CASCADE'), nullable=True, index=True)
    message = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String(2048), nullable=True)
    lineno = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.Float, nullable=False)
    num_warnings = db.Column(db.Integer, nullable=True, default=1)

    __table_args__ = (
        Index('ix_warning_details',
              session_id, test_id, filename, lineno,
              postgresql_where=(session_id == None)), # pylint: disable=singleton-comparison
    )

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE')),
                       db.Index('ix_roles_users_user_id', 'user_id'),
                       UniqueConstraint('user_id', 'role_id'),
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin, TypenameMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True)
    first_name = db.Column(db.String(255), index=True)
    last_name = db.Column(db.String(255), index=True)
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

    __table_args__ = (
        Index('ix_user_first_name_lower', func.lower(first_name)),
        Index('ix_user_last_name_lower', func.lower(last_name)),
    )

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
    edited = db.Column(db.Boolean, server_default="false")

    @rendered_field
    def user_email(self):
        return self.user.email

    @rendered_field(name='user')
    def user_display_nam(self):
        return self.user.display_name()

    @rendered_field
    def can(self):
        is_mine = self.user_id == current_user.id
        return {
            'delete': is_mine,
            'edit': is_mine,
        }


class UserPreference(db.Model):

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    preference = db.Column(db.String(256), nullable=False, primary_key=True)

    value = db.Column(JSONB, nullable=False, default=lambda: {'value': None})

class AppConfig(db.Model):

    key = db.Column(db.String(256), primary_key=True)
    value = db.Column(JSONB, nullable=False)


class Label(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, index=True)


session_label = db.Table('session_label',
                         db.Column('session_id',
                                     db.Integer,
                                     db.ForeignKey('session.id', ondelete='CASCADE')),
                         db.Index('ix_session_label_session_id', 'session_id'),
                         db.Column('label_id',
                                     db.Integer,
                                     db.ForeignKey('label.id', ondelete='CASCADE')),
                        db.Index('ix_session_label_session_id_label_id', 'session_id', 'label_id'),
)


class BackgroundMigration(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), nullable=False)
    started = db.Column(db.Boolean, server_default='FALSE', index=True)
    started_time = db.Column(db.Float)
    finished = db.Column(db.Boolean, server_default='FALSE', index=True)
    finished_time = db.Column(db.Float)
    total_num_objects = db.Column(db.Integer)
    remaining_num_objects = db.Column(db.Integer)
    update_query = db.Column(db.Text(), nullable=False)
    remaining_num_items_query = db.Column(db.Text(), nullable=False)
    batch_size = db.Column(db.Integer, server_default='100000', nullable=False)

    __table_args__ = (
        CheckConstraint("update_query like '%\\:batch_size%'", name='check_has_batch_size'),
    )

    @classmethod
    def get_typename(cls):
        return 'migration'


class Timing(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1024), nullable=False)
    total = db.Column(db.Float(), default=0)

    session_id = db.Column(db.ForeignKey('session.id', ondelete='CASCADE'), nullable=False)
    test_id = db.Column(db.ForeignKey('test.id', ondelete='CASCADE'), nullable=True)

    __table_args__= (
        Index('ix_timing_test', test_id, name, postgresql_where=(test_id != None), unique=True),
        Index('ix_timing_session', session_id, name),
        Index('ix_timing_session_no_test', session_id, name, postgresql_where=(test_id == None), unique=True), # pylint: disable=singleton-comparison
    )


class Replication(db.Model, TypenameMixin):

    STALE_TIMEOUT = 5 * 60

    # identity
    id = db.Column(db.Integer, primary_key=True)
    service_type = db.Column(db.String(50), server_default='elastic-search', nullable=False)
    url = db.Column(db.String(1024), nullable=False)
    index_name = db.Column(db.String(1024), nullable=False, default='backslash')
    username = db.Column(db.String(1024), nullable=True)
    password = db.Column(db.String(1024), nullable=True)
    paused = db.Column(db.Boolean(), server_default='FALSE')

    # indicates whether or not tests remain to be exported for which there is no
    # 'updated_at' value
    untimed_done = db.Column(db.Boolean(), server_default='FALSE')
    backlog_remaining = db.Column(db.Integer(), nullable=True)
    last_replicated_timestamp = db.Column(db.DateTime(), nullable=True)
    last_replicated_id = db.Column(db.Integer, nullable=True)

    last_chunk_finished = db.Column(db.Float, server_default='0')

    last_error = db.Column(db.Text(), nullable=True)
    avg_per_second = db.Column(db.Float(), default=0)

    _client = None

    @rendered_field
    def active(self):
        if self.paused:
            return False
        if self.last_error is not None:
            return False
        return flux.current_timeline.time() - self.last_chunk_finished < self.STALE_TIMEOUT

    def get_client(self):
        from elasticsearch import Elasticsearch
        if self._client is None:
            self._client = Elasticsearch([self.url])
        return self._client
