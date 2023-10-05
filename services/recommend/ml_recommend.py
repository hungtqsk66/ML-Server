from services.recommend.utils.recommend_songs import recommend_songs
from db.mongodb.services.mongo import MongoDB_Service
from utils.Response.response_types import SuccessResponse
from db.redis.init import Redis_DB
import json

class ML_Model:
    def __init__(self) -> None:
        self.db = MongoDB_Service()
        self.cache = Redis_DB.getInstance()
    
    async def recommend(self,song_id:str):
        
        song_cache_value = self.cache.get(song_id)
        
        if song_cache_value : return SuccessResponse(data= json.loads(song_cache_value))
        
        df = await self.db.get_songsStats(song_id)
        
        if df.shape[0] == 0 : return SuccessResponse(data = await self.db.get_songs(song_id=song_id)) 
        
        id_list = recommend_songs(song_id=song_id,data=df)
        
        songs = await self.db.get_songs(id_list=id_list)
        
        self.cache.set(song_id,json.dumps(songs))
        
        return SuccessResponse(data = songs)
    
