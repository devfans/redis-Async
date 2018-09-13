#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis


def try_ignore(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except:
        pass

class Store(object):
    """Initialiaze redis store"""

    prefix = 'redis-store'

    @classmethod
    def initialize(cls, **options):
        cls.redisUrl = options.get('url') or 'redis://localhost:6379'
        if 'prefix' in options:
            cls.prefix = options['prefix']
        cls.client = cls.getClient()

    @classmethod
    def getClient(cls):
        pool = redis.ConnectionPool.from_url(cls.redisUrl)
        client = redis.StrictRedis(connection_pool=pool)
        return client

    @classmethod
    def getPipeline(cls, **kwargs):
        transaction = kwargs.get('transaction', True)
        return cls.client.pipeline(transaction=transaction)


class RedisKey(object):
    """General redis key"""

    def __init__(self, **kwargs):
        if 'tpl' not in kwargs:
            raise Exception("Template(tpl) needed for redis keys")
        self._tpl = kwargs['tpl']
        self._expire = kwargs.get('exp', None)

    def _key(self, kwargs):
        return Store.prefix + ':' + self._tpl.format(**kwargs)

    def _reset(self, key, exp=None):
        expire = exp or self._expire
        if expire is not None:
            try_ignore(Store.client.expire, key, int(expire))

    def ttl(self, **kwargs):
        return Store.client.ttl(self._key(kwargs))

    async def ttlAsync(self, **kwargs):
        return Store.client.ttl(self._key(kwargs))

    def expire(self, *args, **kwargs):
        delta = args[0] if len(args) > 0 else self._expire
        try:
            Store.client.expire(self._key(kwargs), int(delta))
        except:
            pass

    async def expireAsync(self, *args, **kwargs):
        return self.expire(*args, **kwargs)

    def delete(self, **kwargs):
        return Store.client.delete(self._key(kwargs))

    async def deleteAsync(self, **kwargs):
        return Store.client.delete(self._key(kwargs))

    def exists(self, **kwargs):
        return Store.client.exists(self._key(kwargs))

    async def existsAsync(self, **kwargs):
        return Store.client.exists(self._key(kwargs))



class RedisList(RedisKey):
    def lrange(self, l, r, **kwargs):
        return Store.client.lrange(self._key(kwargs), l, r)

    async def lrangeAsync(self, l, r, **kwargs):
        return Store.client.lrange(self._key(kwargs), l, r)

    def rpush(self, value, **kwargs):
        return Store.client.rpush(self._key(kwargs), value)

    async def rpushAsync(self, value, **kwargs):
        return Store.client.rpush(self._key(kwargs), value)

    def lrem(self, value, count=1, **kwargs):
        return Store.client.lrem(self._key(kwargs), value, count)

    async def lrem(self, value, count=1, **kwargs):
        return Store.client.lrem(self._key(kwargs), value, count)



class RedisString(RedisKey):
    def get(self, **kwargs):
        return Store.client.get(self._key(kwargs))

    def getAsync(self, **kwargs):
        return Store.client.get(self._key(kwargs))

    def set(self, value, **kwargs):
        extra = []
        if self._expire is not None:
            extra = ['EX', self._expire]
        return Store.client.set(self._key(kwargs), value, *extra)

    def setnx(self, value, **kwargs):
        extra = []
        if self._expire is not None:
            extra = ['EX', self._expire]

        return Store.client.setnx(self._key(kwargs), value, *extra)

    async def setAsync(self, value, **kwargs):
        return self.set(value, **kwargs)

    async def setnxAsync(self, value, **kwargs):
        return self.setnx(value, **kwargs)


class RedisSet(RedisKey):
    pass

class RedisSSet(RedisKey):
    pass


class RedisHash(RedisKey):

    def hget(self, field, **kwargs):
        return Store.client.hget(self._key(kwargs), field)

    async def hget(self, field, **kwargs):
        return Store.client.hget(self._key(kwargs), field)

    def hset(self, field, value, **kwargs):
        Store.client.hset(self._key(kwargs), field, value)

    async def hsetAsync(self, field, value, **kwargs):
        Store.client.hset(self._key(kwargs), field, value)


    def hmset(self, value, **kwargs):
        key = self._key(kwargs)
        Store.client.hmset(key, value)
        self._reset(key)

    async def hmsetAsync(self, value, **kwargs):
        self.hmset(value, **kwargs)

    def hsetnx(self, field, value, **kwargs):
        return Store.client.hsetnx(self._key(kwargs), field, value)

    async def hsetnxAsync(self, field, value, **kwargs):
        return Store.client.hsetnx(self._key(kwargs), field, value)

    def hexists(self, field, **kwargs):
        return Store.client.hexists(self._key(kwargs), field)

    async def hexistsAsync(self, field, **kwargs):
        return Store.client.hexists(self._key(kwargs), field)

    def hkeys(self, **kwargs):
        return Store.client.hkeys(self._key(kwargs))

    async def hkeysAsync(self, **kwargs):
        return Store.client.hkeys(self._key(kwargs))

    def hgetall(self, **kwargs):
        return Store.client.hgetall(self._key(kwargs))

    async def hgetallAsync(self, **kwargs):
        return Store.client.hgetall(self._key(kwargs))



# def async_call(methods):
#     def async_call_wrapper(Kls):
#         class AsyncKls(object):
#             def __init__(*args, **kwargs):
#                 self.__instance = Kls(*args, **kwargs)
# 
#             def __getattribute__(self, attr):
#                 if attr not in methods:
#                     return self.__instance.__getattribute__(attr)
# 
#                 async def method(*args, **kwargs):
#                     return self.__instance.__getattribute__(attr)(*args, **kwargs)
# 
#                 return _method



# class Singleton(type):
#     _instances = {}
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]

