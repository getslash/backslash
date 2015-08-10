import functools

import inflect

_caches = {}
_english = inflect.engine()


def _memoized(func):
    func_name = func.__name__
    @functools.wraps(func)
    def new_func(arg):
        cache = _caches.get(func_name)
        if cache is None:
            cache = _caches[func_name] = {}
        value = cache.get(arg)
        if value is None:
            value = cache[arg] = func(arg)
        return value
    return new_func

plural_noun = _memoized(_english.plural_noun)

