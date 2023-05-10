#!/usr/bin/env python3
''' 
create a web cache
'''
import requests
import redis
from functools import wraps


db = redis.Redis()


def count_page_access(method):
    ''' count number of time a website is accessed '''
    @wraps(method)
    def func(url):
        ''' wrap function '''
        ckey = 'cached:' + url
        cdata = db.get(ckey)
        if cdata:
            return cdata.decode('utf-8')

        key = 'count:' + url
        db.incr(key)
        page = method(url)
        db.set(ckey, page)
        db.expire(ckey, 10)
        return page
    return func


@count_page_access
def get_page(url: str) -> str:
    ''' fetch content from url '''
    return requests.get(url).text
