from flask.ext.security import current_user


ACTION_ARCHIVED, ACTION_UNARCHIVED, MAX_ACTIVITY = range(3)

_ACTION_STRINGS = {
    ACTION_ARCHIVED: 'archived',
    ACTION_UNARCHIVED: 'unarchived',
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

