from uuid import uuid4

import requests

from flask import Blueprint, abort, jsonify, request, url_for
from flask_security.core import current_user
from flask_security.decorators import login_required
from urlobject import URLObject as URL

from ..models import RunToken, db
from ..utils.redis import get_redis_client

_REDIS_TOKEN_TTL = 15 * 60
_REDIS_REQUEST_TTL = 5 * 60

blueprint = Blueprint('runtoken', __name__)


@blueprint.route('/runtoken/request/new')
@blueprint.route('/runtoken/request/<request_id>')
def runtoken_request(request_id=None):
    if request_id is None:
        request_id = _create_new_runtoken_request()

    return _get_runtoken_request_status(request_id)


@blueprint.route('/runtoken/request/<request_id>/complete', methods=['POST'])
@login_required
def complete_runtoken_request(request_id):
    redis = get_redis_client()
    key = _get_request_key(request_id)
    if redis.get(key) is None:
        abort(requests.codes.not_found) # pylint: disable=no-member

    token = create_new_runtoken(current_user)
    db.session.commit()
    # set reply
    redis.set(name=key, value=token, ex=_REDIS_TOKEN_TTL)
    return 'success'


def create_new_runtoken(user):
    token = '{}:{}'.format(user.id, uuid4())
    db.session.add(RunToken(
        user_id=user.id,
        token=token))
    return token



def _create_new_runtoken_request():
    request_id = str(uuid4())
    redis = get_redis_client()
    redis.set(name=_get_request_key(request_id), value='', ex=_REDIS_TOKEN_TTL)
    return request_id

def _get_request_key(request_id):
    return 'request:{}'.format(request_id)

def _get_runtoken_request_status(request_id):
    request_key = 'request:{}'.format(request_id)
    value = get_redis_client().get(request_key)
    if value is None:
        abort(requests.codes.not_found) # pylint: disable=no-member
    return jsonify({
        'token': value.decode('utf-8'),
        'url': URL(request.host_url).add_path(url_for('runtoken.runtoken_request', request_id=request_id)),
        'complete': request.host_url + '#/runtoken/' + request_id + '/authorize',
    })
