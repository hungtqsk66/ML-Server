from pymongo import MongoClient
from decouple import config


class MongoDB:
    _instance = None

    @staticmethod
    def getInstance():
        if MongoDB._instance is None:
            MongoDB()
        return MongoDB._instance

    def __init__(self):
        if MongoDB._instance is not None:
            raise Exception("This is a singleton class!")
        else:
            MongoDB._instance = MongoClient(config('IP'),int(config('PORT')))
    