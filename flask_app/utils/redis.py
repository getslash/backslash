import os
from redis import Redis


_redis_client = None

def get_redis_client():
    global _redis_client        # pylint: disable=global-statement
    if _redis_client is None:
        _redis_client = Redis(os.environ.get('BACKSLASH_REDIS_SERVER'))
    return _redis_client
