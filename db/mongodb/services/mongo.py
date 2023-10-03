from db.mongodb.init import MongoDB
from bson.objectid import ObjectId


class MongoDB_Service():
    
    def __init__(self):
        self.db = MongoDB.getInstance()['audioServerDev']
        
    def serializeDocuments(self,documents:list)->list:
        for doc in documents:
            doc['_id'] = str(doc['_id'])
        return documents
    
    
    async def get_songsStats(self,song_id:str):
        collection = self.db['Songs-Stats']
        result = collection.find_one({'_id':ObjectId(song_id)})
        if not result : return []
        genre = result['genre']
        return collection.find({"genre":{"$in":genre}})
        
    
    
    async def get_songs(self,id_list:list=None,song_id=None)->list:
        
        collection = self.db['Songs']
        if not id_list :
            results =  list(collection.aggregate([
                {"$match":{"_id":{"$ne":ObjectId(song_id)}}},
                {"$sample": { "size": 12 } }
            ]))
    
        else:
            object_ids = [ObjectId(id) for id in id_list]
        
            results = list(collection.find({'_id':{'$in':object_ids}}))
        

        return self.serializeDocuments(results)
        