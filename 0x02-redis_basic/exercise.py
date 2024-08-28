#!/usr/bin/env python3
"""Writing strings to Redis"""


import uuid
import redis
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count how many times methods of the Cache class are called"""
    @wraps(method)
    def counter(self, *args, **kwargs):
        """increments the count for that key every time the method is called"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return counter


class Cache:
    """This a class called Cache"""
    def __init__(self):
        """initializing Redis client and soring in a private var"""
        self._redis = redis.Redis()

        self._redis.flushdb()


    @count_calls    
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores data in Redis using random key and returns the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[bytes, str, int, float]:
        """
        takes key str argument and fn callaable optional argument used to covert
        data to desired format
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data


    def get_str() -> Optional[str]:
        """Retrieve the data as a UTF-8 string"""
        return self.get(key, fn=lambda x: x.decode('utf-8'))


    def get_int() -> Optional[int]:
        """Retrieves data as an integer"""
        return self.get(key, fn=lambda x: int(x))
