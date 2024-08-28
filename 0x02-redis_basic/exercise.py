#!/usr/bin/env python3
"""Writing strings to Redis"""


import uuid
import redis
from typing import Union


class Cache:
    """This a class called Cache"""
    def __init__(self):
        """initializing Redis client and soring in a private var"""
        self._redis = redis.Redis()

        self._redis.flushdb()


    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores data in Redis using random key and returns the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
