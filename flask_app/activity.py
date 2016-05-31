import functools

import flux

from flask import g

from sqlalchemy.sql import select, union_all, literal_column
from sqlalchemy import and_

from flask.ext.security import current_user



ACTION_ARCHIVED, ACTION_UNARCHIVED, ACTION_INVESTIGATED, ACTION_UNINVESTIGATED, MAX_ACTIVITY, ACTION_COMMENTED = range(6)

_ACTION_STRINGS = {
    ACTION_COMMENTED: 'commented',
    ACTION_ARCHIVED: 'archived',
    ACTION_UNARCHIVED: 'unarchived',
    ACTION_INVESTIGATED: 'investigated',
    ACTION_UNINVESTIGATED: 'uninvestigated',
}

def register_user_activity(action, **kw):
    from . import models
    assert action < MAX_ACTIVITY
    models.db.session.add(
        models.Activity(
            action=action,
            user_id=current_user.id,
            **kw))

def get_action_string(action):
    return _ACTION_STRINGS.get(action)


def get_activity_query(user_id=None, session_id=None, test_id=None):
    # pylint: disable=no-member
    from .models import Activity, Comment, User

    _filter = functools.partial(_apply_filters, user_id=user_id, session_id=session_id, test_id=test_id)

    comments = select([
        literal_column("('comment:' || comment.id)").label('id'),
        literal_column(str(ACTION_COMMENTED)).label('action'),
        Comment.user_id.label('user_id'),
        Comment.session_id.label('session_id'),
        Comment.test_id.label('test_id'),
        Comment.timestamp.label('timestamp'),
        Comment.comment.label('text'),
        (User.first_name + ' ' + User.last_name).label('user_name'),
        User.email.label('user_email'),
    ]).select_from(Comment.__table__.join(User, User.id == Comment.user_id))

    comments = _filter(Comment, comments)

    activity = select([
        literal_column("('activity:' || activity.id)").label('id'),
        Activity.action.label('action'),
        Activity.user_id.label('user_id'),
        Activity.session_id.label('session_id'),
        Activity.test_id.label('test_id'),
        Activity.timestamp.label('timestamp'),
        literal_column("NULL").label('text'),
        (User.first_name + ' ' + User.last_name).label('user_name'),
        User.email.label('user_email'),
    ]).select_from(Activity.__table__.join(User, User.id == Activity.user_id))

    activity = _filter(Activity, activity)

    u = union_all(comments, activity).alias('u')

    return select([u]).order_by(u.c.timestamp)


def _apply_filters(model, query, **filters):
    whereclause = []

    for key, value in filters.items():
        if value is None:
            continue
        whereclause.append(getattr(model, key) == value)
    return query.where(and_(*whereclause))


def updates_last_active(func):
    from . import models

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        if hasattr(g, 'token_user'):
            u = g.token_user
        elif current_user.is_authenticated:
            u = models.User.query.get(current_user.id)
        else:
            u = None

        if u is not None:
            u.last_activity = flux.current_timeline.time()
            models.db.session.add(u)
        return func(*args, **kwargs)

    return new_func
