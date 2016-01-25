from uuid import uuid4

from flask import Blueprint, jsonify, redirect, request, url_for
from flask.ext.security.decorators import login_required
from flask.ext.security.core import current_user

from ..models import db, RunToken

from redis import Redis
from urlobject import URLObject as URL

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
    redis = _get_redis_client()
    key = _get_request_key(request_id)
    if redis.get(key) is None:
        abort(requests.codes.not_found)

    token = create_new_runtoken(user)
    db.session.commit()
    # set reply
    redis.setex(key, token, _REDIS_TOKEN_TTL)
    return 'success'


def create_new_runtoken(user):
    token = '{}:{}'.format(user.id, uuid4())
    db.session.add(RunToken(
        user_id=user.id,
        token=token))
    return token



def _create_new_runtoken_request():
    request_id = str(uuid4())
    _get_redis_client().setex(
        _get_request_key(request_id), '', _REDIS_REQUEST_TTL)
    return request_id

def _get_request_key(request_id):
    return 'request:{}'.format(request_id)

def _get_runtoken_request_status(request_id):
    request_key = 'request:{}'.format(request_id)
    value = _get_redis_client().get(request_key)
    if value is None:
        abort(requests.codes.not_found)
    return jsonify({
        'token': value,
        'url': URL(request.host_url).add_path(url_for('runtoken.runtoken_request', request_id=request_id)),
        'complete': request.host_url + '#/runtoken/' + request_id + '/authorize',
    })

def _get_redis_client():
    return Redis()
