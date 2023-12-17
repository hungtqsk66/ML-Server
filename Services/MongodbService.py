from DB.mongodb.init import MongoDB
from bson.objectid import ObjectId
import pandas as pd


class DBService():
    
    def __init__(self):
        self.db = MongoDB.getInstance()['audioServerDev']
        
    def serializeDocuments(self,documents:list)->list:
        for doc in documents:
            doc['_id'] = str(doc['_id'])
        return documents
    
    
    async def get_songsStats(self,song_id:str)->pd.DataFrame:
        
        collection = self.db['Songs-Stats']
        
        result = await collection.find_one({'_id':ObjectId(song_id)})
        
        if result is None : return pd.DataFrame()
        
        df = pd.DataFrame.from_records([result])
        
        genre = result['genre']
    
        if len(genre) == 0 : 
            cursor = collection.aggregate(
                {
                    "$match":{
                        "genre":[],
                        '_id':{"$ne":ObjectId(song_id)}
                    }
                }
                ,
                {"$sample":{"size":80}
            })
            
            df = df.append(pd.DataFrame.from_records(await cursor.to_list(None)),ignore_index=True)
            df['genre'] = "None"
           
               
        else : 
            cursor = collection.aggregate([
                    {
                        "$match":{"genre":{"$in":genre},'_id':{"$ne":ObjectId(song_id)}}
                    },
                    {
                        "$sample":{"size":80}
                    }
                ])
     
            df = df.append(pd.DataFrame.from_records(await cursor.to_list(None)),ignore_index=True)
        
            
        df['_id'] = df['_id'].astype(str)

        df['genre'] = df['genre'].astype(str)
        
        return df




        
    
    
    async def get_songs(self,id_list:list=None,exclude_id=None)->list:
        
        collection = self.db['Songs']
        
        cursor = None
        
        if not id_list :
            cursor =  collection.aggregate([
                {"$match":{"_id":{"$ne":ObjectId(exclude_id)}}},
                {"$sample": { "size": 12 } }
            ])
            
        else:
            object_ids = [ObjectId(id) for id in id_list]
        
            cursor =collection.find({'_id':{'$in':object_ids}})
            
        if cursor == None: return []
        
        return self.serializeDocuments(await cursor.to_list(None))

        