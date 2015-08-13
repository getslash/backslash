from flask.ext.security import current_user


ACTION_ARCHIVED, ACTION_UNARCHIVED, ACTION_INVESTIGATED, ACTION_UNINVESTIGATED, MAX_ACTIVITY = range(5)

_ACTION_STRINGS = {
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

