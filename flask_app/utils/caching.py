from dogpile.cache import make_region

HOURS = 60 * 60

cache = make_region(key_mangler='backslash:cache:{}'.format).configure(
    'dogpile.cache.redis',
    arguments = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
        'redis_expiration_time': 2 * HOURS,
        'distributed_lock': True
        }
)

