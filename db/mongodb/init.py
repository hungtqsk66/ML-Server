from decouple import config #type:ignore
import motor.motor_asyncio 


class MongoDB:
    _instance = None
    #To use this class please call the get instance method along with the [database name] + [collection name] (optional)
    @staticmethod
    def getInstance():
        if MongoDB._instance is None:
            MongoDB()
        return MongoDB._instance

    def __init__(self):
        if MongoDB._instance is not None:
            raise Exception("This is a singleton class!")
        else:
            MongoDB._instance = motor.motor_asyncio.AsyncIOMotorClient(config('IP'),int(config('PORT')))
    