#!/usr/bin/env python3
"""Web caching module with URL access tracking."""

import redis
import requests
from typing import Callable
from functools import wraps

# Initialize Redis client
redis_client = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called."""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function to increment call count."""
        key = f"count:{url}"
        redis_client.incr(key)
        return method(url)
    return wrapper


def cache_result(expiration: int = 10) -> Callable:
    """Decorator to cache the result of a function in Redis."""
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


@count_calls
@cache_result(expiration=10)
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL and cache it."""
    response = requests.get(url)
    return response.text
