import functools

from flask import Blueprint
from flask.ext.simple_api import SimpleAPI

from ... import activity
from ...utils.api_utils import (auto_render, requires_login,
                                requires_login_or_runtoken)

blueprint = Blueprint('api', __name__, url_prefix='/api')

api = SimpleAPI(blueprint)

def API(func=None, require_real_login=False, generates_activity=True, require_login=True):
    if func is None:
        return functools.partial(API, require_real_login=require_real_login, generates_activity=generates_activity, require_login=require_login)

    returned = auto_render(func)

    if generates_activity:
        returned = activity.updates_last_active(returned)

    if require_login:
        if require_real_login:
            returned = requires_login(returned)
        else:
            returned = requires_login_or_runtoken(returned)
    return api.include(returned)
