from db.mongodb.init import MongoDB
from bson.objectid import ObjectId
from pandas import DataFrame
from typing import Optional
from jose import jwt# type: ignore
from decouple import config #type:ignore

class DBService():
    
    def __init__(self):
        self.db = MongoDB.getInstance()[str(config('DATABASE'))]
        
    def __serializeDocuments(self,documents:list)->list:
        for doc in documents:
            doc['_id'] = str(doc['_id'])
            doc['artist'] = [str(id) for id in doc['artist']]
        return documents
    
    #This function only used for Cosine Similarity that get maximum 80 random songs that share similar genre
    async def GetSongsStats(self,song_id:str)->DataFrame:
        
        collection = self.db['Songs-Stats']
        
        result = await collection.find_one({'_id':ObjectId(song_id)})
        
        if result is None : return DataFrame()
        
        df = DataFrame.from_records([result])
        
        genre:list[str] = result['genre']
    
        if len(genre) == 0 : 
            cursor = collection.aggregate([
                {
                    "$match":{
                        "genre":[],
                        '_id':{"$ne":ObjectId(song_id)}
                    }
                }
                ,
                {"$sample":{"size":80}}
            ])
                   
            df = df.append(DataFrame.from_records(await cursor.to_list(None)),ignore_index=True) # type: ignore
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
     
            df = df.append(DataFrame.from_records(await cursor.to_list(None)),ignore_index=True) # type: ignore
        
        df['_id'] = df['_id'].astype(str)
        df['genre'] = df['genre'].astype(str)
            
        return df

        

    #This function only used to get the songs-stats for model prediction
    async def GetAllSongsStats(self,id_list:list)->list:
        
        collection = self.db['Songs-Stats']
        filter = {'mode':0,'duration_ms':0,'time_signature':0,'genre':0}
        cursor = collection.find({"_id":{"$nin":id_list}},filter)
        
        return await cursor.to_list(None)  
    
    
     #This function only used to get the songs metadata return to frontend client 
    async def GetSongs(self,id_list:Optional[list] = None,exclude_id=None)->list:
        
        collection = self.db['Songs']
        
        cursor = None
        
        if id_list is None:
            cursor =  collection.aggregate([
                {"$match":{"_id":{"$ne":ObjectId(exclude_id)}}},
                {"$sample": { "size": 12 } }
            ])
            
        else:
            object_ids = [ObjectId(id) for id in id_list]
        
            cursor =collection.find({'_id':{'$in':object_ids}})
            
        if cursor == None: return []
        
        return self.__serializeDocuments(await cursor.to_list(None))
    
    
    
    #This function only used to get the songs-stats and also songs that user have listened for model creation
    async def GetUserItemsRecord(self,user_id:str | None )->list:
        
        collection = self.db['Users-Items']
        
        cursor = collection.aggregate(
            [
                {
                    "$match":{"_id":ObjectId(user_id)}
                },
                {
                    "$lookup": {
                    "from": 'Songs-Stats',
                    "localField":'records.song_id' ,
                    "foreignField": '_id',
                    "as": 'Songs-Stats'
                    }
                }
            ]
        )
        return await cursor.to_list(None)
    
    async def ValidateAccessToken(self,user_id:str | None,accessToken:str | None)-> bool:
        
        collection = self.db['Keys']
        userAuthKeys = await collection.find_one({"user":ObjectId(user_id)})
        if userAuthKeys is None: return False
        secret:str = userAuthKeys['publicKey']
        decodedUser:dict = jwt.decode(accessToken,secret)
        return decodedUser['userId'] == user_id 
        
        
        
        
        
        
        
        
    
    
    

        