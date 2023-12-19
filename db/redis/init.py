#import redis.asyncio as redis
from redis import asyncio as aioredis

class RedisDB:
    _instance = None
    #To use this class simply call the getInstance method . The default redis connection would be local DB 
    @staticmethod
    def getInstance():
        if RedisDB._instance is None:
            RedisDB()
        return RedisDB._instance

    def __init__(self):
        if RedisDB._instance is not None:
            raise Exception("This is a singleton class!")
        else:
            RedisDB._instance = aioredis.from_url("redis:127.0.0.1:6379").client()