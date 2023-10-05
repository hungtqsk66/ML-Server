from redis import Redis

class Redis_DB:
    _instance = None

    @staticmethod
    def getInstance():
        if Redis_DB._instance is None:
            Redis_DB()
        return Redis_DB._instance

    def __init__(self):
        if Redis_DB._instance is not None:
            raise Exception("This is a singleton class!")
        else:
            Redis_DB._instance = Redis(host='127.0.0.1',port=6379)