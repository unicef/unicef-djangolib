import uuid
from functools import wraps

from django.core.cache import cache
from django.db import connection
from django.utils.cache import patch_cache_control
from rest_framework import status
from rest_framework.response import Response


def etag_cached(cache_key, public_cache=False):
    """
    Returns list of instances only if there's a new ETag, and it does not
    match the one sent along with the request.
    # Otherwise it returns 304 NOT MODIFIED.
    """

    def make_cache_key():
        if public_cache:
            schema_name = 'public'
        else:
            schema_name = getattr(connection, 'schema_name', 'public')

        return f'{schema_name}-{cache_key}-etag'

    def decorator(func):

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            key = make_cache_key()

            cache_etag = cache.get(key)
            request_etag = self.request.META.get("HTTP_IF_NONE_MATCH", None)

            local_etag = cache_etag if cache_etag else uuid.uuid4().hex

            if cache_etag and request_etag and cache_etag == request_etag:
                response = Response(status=status.HTTP_304_NOT_MODIFIED)
            else:
                response = func(self, *args, **kwargs)
                response["ETag"] = local_etag

            if not cache_etag:
                cache.set(key, local_etag)

            patch_cache_control(response, private=True, must_revalidate=True)
            return response

        def invalidate():
            cache.delete(make_cache_key())

        wrapper.invalidate = invalidate
        return wrapper
    return decorator
