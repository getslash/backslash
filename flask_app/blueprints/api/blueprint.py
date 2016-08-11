import functools

from flask import Blueprint
from flask_simple_api import SimpleAPI

from ... import activity
from ...utils.api_utils import (auto_render, requires_login,
                                requires_login_or_runtoken)

blueprint = Blueprint('api', __name__, url_prefix='/api')

api = SimpleAPI(blueprint)

_api_info = {'endpoints': {}}


def API(func=None, require_real_login=False, generates_activity=True, require_login=True, version=1):
    if func is None:
        return functools.partial(API, require_real_login=require_real_login, generates_activity=generates_activity, require_login=require_login, version=version)

    returned = auto_render(func)

    endpoint_info = _api_info['endpoints'][func.__name__] = {}
    endpoint_info['login_required'] = require_login
    endpoint_info['version'] = version

    if generates_activity:
        returned = activity.updates_last_active(returned)

    if require_login:
        if require_real_login:
            returned = requires_login(returned)
        else:
            returned = requires_login_or_runtoken(returned)
    return api.include(returned)


@blueprint.route('/', methods=['OPTIONS'], strict_slashes=False)
def get_api_info():
    from flask import jsonify
    return jsonify(_api_info)
