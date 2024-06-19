#!/usr/bin/env python3
'''
Module handling the method "store" that generates a random key
'''
import redis
import uuid
from typing import Union, Callable, Optional
import functools


def count_calls(methods: Callable) -> Callable:
    '''
    Decorator that counts the number of calls to a method.
    '''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''
    Decorator to store the history of inputs and outputs for a function
    '''
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper


def replay(method: Callable):
    '''
    Display the history of calls of a particular function.
    '''
    redis_client = method.__self__._redis
    method_qualname = method.__qualname__

    inputs = redis_client.lrange(f"{method_qualname}:inputs", 0, -1)
    outputs = redis_client.lrange(f"{method_qualname}:outputs", 0, -1)

    print(f"{method_qualname} was called {len(inputs)} times:")

    for input, output in zip(inputs, outputs):
        print(f"{method_qualname}(*{input.decode('utf-8')}) -> {output.decode('utf-8')}")


class Cache:
    def __init__(self):
        '''
        Initialize the Redis client and flush the database.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        Store data in Redis with a random key and return the key.
        '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes,
                                                    int, float, None]:
        '''
        Retrieve data from Redis and apply an
        optional callable to convert the data.
        '''
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        '''
        Retrieve data from Redis and convert it to a string.
        '''
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        '''
        Retrieve data from Redis and convert it to an integer.
        '''
        return self.get(key, fn=int)
