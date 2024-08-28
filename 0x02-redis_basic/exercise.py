#!/usr/bin/env python3
"""Writing strings to Redis"""


import uuid
import redis
import json
from typing import Union, Callable, Optional, Any
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


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs for a particular function"""
    @wraps(method)
    def wrapper(self, *args):
        """store the history of inputs and outputs for a particular function"""
        input_keys = f'{method.__qualname__}:inputs'
        output_keys = f'{method.__qualname__}:outputs'
        self._redis.rpush(input_keys, str(args))
        output = method(self, *args)
        self._redis.rpush(output_keys, str(output))
        return output
    return wrapper


class Cache:
    """This a class called Cache"""
    def __init__(self):
        """initializing Redis client and soring in a private var"""
        self._redis = redis.Redis()

        self._redis.flushdb()


    @count_calls
    @call_history
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
