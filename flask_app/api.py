from flask import Blueprint, request

from .api_utils import get_api_decorator, auto_add_object
from .models import db, Session
from weber_utils import takes_schema_args, Optional

blueprint = Blueprint('api', __name__)

api_func = get_api_decorator(blueprint)

##########################################################################


@api_func
@auto_add_object
@takes_schema_args(hostname=Optional(str))
def report_session_start(hostname=None):
    if hostname is None:
        hostname = request.remote_addr
    return Session(hostname=hostname)
