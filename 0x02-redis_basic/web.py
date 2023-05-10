#!/usr/bin/env python3
"""contains a function that obtains html from web"""
import requests
import redis
import functools
from typing import Callable


def count_calls(fn: Callable) -> Callable:
    """counts call to a function"""
    @functools.wraps(fn)
    def wrapper(url, *args, **kwargs):
        r = redis.Redis()
        key = 'count:' + url
        r.incr(key)
        return fn(url, *args, **kwargs)
    return wrapper


def cache_fn(fn: Callable) -> Callable:
    """caches the function call"""
    @functools.wraps(fn)
    def wrapper(url, *args, **kwargs):
        r = redis.Redis()
        key = 'content:' + url
        cache = r.get(key)
        if cache:
            return cache
        result = fn(url, *args, **kwargs)
        r.setex('content:' + url, 10, result)
        return result
    return wrapper


@count_calls
@cache_fn
def get_page(url: str) -> str:
    """obtains the HTML content of a particular URL and returns it"""
    res = requests.get(url)
    return res.text
