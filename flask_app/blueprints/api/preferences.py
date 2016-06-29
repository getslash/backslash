import json
from numbers import Number

from flask import current_app
from flask_security import current_user

from ...models import UserPreference, db
from .blueprint import API

NoneType = type(None)


@API(require_real_login=True)
def get_preferences():
    user_id = current_user.id
    returned = dict(current_app.config['DEFAULT_PREFERENCES'])
    for pref in UserPreference.query.filter_by(user_id=user_id):
        returned[pref.preference] = pref.value['value']
    return returned


@API(require_real_login=True)
def set_preference(preference: str, value: (str, Number)):
    user_id = current_user.id

    db.session.execute('''
    INSERT INTO user_preference (user_id, preference, value)
    VALUES (:user_id, :pref, :value)
    ON CONFLICT (user_id, preference) DO UPDATE SET value=EXCLUDED.value
    ''', params={
        'user_id': user_id,
        'pref': preference,
        'value': json.dumps({'value': value})
    })
    db.session.commit()
    return value


@API(require_real_login=True)
def unset_preference(preference: str):
    user_id = current_user.id
    UserPreference.query.filter_by(
        user_id=user_id, preference=preference).delete()
    db.session.commit()
