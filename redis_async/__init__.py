#!/usr/bin/env python
# -*- coding: utf-8 -*-

__VERSION__ = '0.0.1'
version_info = (0, 0, 1)

from redis_async.Dal import Store as Redis
from redis_async.Dal import RedisKey, RedisHash, RedisString, RedisList, RedisSet, RedisSSet

__all__ = ['Redis', 'RedisKey', 'RedisHash', 'RedisString', 'RedisList', 'RedisSet', 'RedisSSet']


