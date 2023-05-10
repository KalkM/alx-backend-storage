"""Implements a get page function"""
import redis
import requests


def get_page(url: str) -> str:
    """Tracks the amount of times a url is called"""
    r = redis.Redis()
    key = 'count:' + url
    if not r.get(key):
        r.setex('count:'+url, 10, 1)
    else:
        r.incr(key, 1)

    return requests.get(url).content.decode()
