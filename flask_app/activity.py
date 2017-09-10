import functools

import flux

from flask import g

from flask_security import current_user


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
            u.last_activity = flux.current_timeline.time() # pylint: disable=no-member
            models.db.session.add(u)
        return func(*args, **kwargs)

    return new_func
