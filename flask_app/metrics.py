from flask import Blueprint, Response
from .utils.redis import get_redis_client

_stats = []

class Counter:

    TYPE = 'gauge'
    def __init__(self, name, help_message):
        self.name = name
        self.help_message = help_message
        self.redis_key = f'stat_{self.name}'
        _stats.append(self)

    def increment(self):
        get_redis_client().incr(self.redis_key)

    def get(self):
        return int(get_redis_client().get(self.redis_key) or 0)


num_new_sessions = Counter('num_new_sessions', 'Number of sessions created since Backslash came up')
num_new_tests = Counter('num_new_tests', 'Number of tests started since Backslash came up')

metrics_blueprint = Blueprint('metrics', __name__)

@metrics_blueprint.route('/metrics')
def get_metrics():
    returned = ""
    for stat in _stats:
        metric_name = f'backslash_{stat.name}'
        returned += f'# HELP {metric_name} {stat.help_message}\n# TYPE {metric_name} {stat.TYPE}\n'
        returned += f'{metric_name} {stat.get()}\n'
    return Response(returned, mimetype='text/plain')
