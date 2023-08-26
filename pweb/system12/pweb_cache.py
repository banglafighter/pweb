import functools
import gc
from datetime import timedelta, datetime
from functools import lru_cache, wraps

CACHE_1_MINUTES = 60
CACHE_30_MINUTES = CACHE_1_MINUTES * 30
CACHE_1_HOUR = CACHE_1_MINUTES * 60
CACHE_1_DAY = CACHE_1_HOUR * 24
CACHE_1_MONTY = CACHE_1_DAY * 30
CACHE_1_YEAR = CACHE_1_DAY * 364


class PWebCache:
    enableCache: bool = True

    @staticmethod
    def clean_all():
        gc.collect()
        objects = [i for i in gc.get_objects() if isinstance(i, functools._lru_cache_wrapper)]
        if objects:
            for cache_object in objects:
                cache_object.cache_clear()


def pweb_cache(seconds: int = CACHE_30_MINUTES, maxsize: int = 128):
    def wrapper_cache(func):
        if PWebCache.enableCache:
            func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime

            return func(*args, **kwargs)

        return wrapped_func
    return wrapper_cache
