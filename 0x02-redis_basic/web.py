#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""

import redis
import requests
from typing import Callable
from functools import wraps
from exercise import count_calls


redis_client = redis.Redis()


def cache_result(expiration: int = 10) -> Callable:
    """Decorator to cache the result of a function in redis."""
    def decorator(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(url: str) -> str:
            """Wrapper function to cache the result."""
            cached_result = redis_client.get(url)
            if cached_result:
                return cached_result.decode('utf-8')

            result = method(url)
            redis_client.setex(url, expiration, result)
            return result
        return wrapper
    return decorator


@count_calls  # Using the imported count_calls decorator
@cache_result(expiration=10)
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL and cache it."""
    response = requests.get(url)
    return response.text
