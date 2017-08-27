# -*- coding: utf-8 -*-
import redis, sys
from cmdb import configs

class MQ():

    def __init__(self, channel, host=configs.REDIS_HOST, port=6379):
        self.__conn = redis.Redis(host=host, port=port)
        self.channel = channel

    def publish(self, msg, channel=''):
        if not channel:
            channel = self.channel
        self.__conn.publish(channel, msg)

    def subscribe(self, channel=''):
        if not channel:
            channel = self.channel
        pub = self.__conn.pubsub()
        pub.subscribe(channel)
        return pub.listen()

class Q():
    def __init__(self, key, host=configs.REDIS_HOST, port=6379):
        self.__conn = redis.Redis(host=host, port=port)
        self.key = key

    def push(self, msg, key=''):
        if not key:
            key = self.key
        self.__conn.lpush(key, msg)

    def pop(self, key=''):
        if not key:
            key = self.key
        return self.__conn.blpop(key)

class RedisHealthCheck():
    state = False
    def __init__(self, host=configs.REDIS_HOST, port=6379):
        try:
            self.__conn = redis.Redis(host=host, port=port)
            self.state = True
        except Exception as ex:
            print str(ex)
            self.state = False