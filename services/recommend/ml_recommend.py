import pandas as pd
from services.recommend.utils.recommend_songs import recommend_songs
from db.mongodb.services.mongo import MongoDB_Service
from utils.Response.response_types import SuccessResponse

class ML_Model:
    def __init__(self) -> None:
        self.db = MongoDB_Service()
    
    async def recommend(self,song_id:str):
        
        df = pd.DataFrame.from_records(await self.db.get_songsStats(song_id))
        
        if df.shape[0] == 0 : return SuccessResponse(data = await self.db.get_songs(song_id=song_id)) 
        
        df['_id'] = df['_id'].astype(str)
        
        df['genre'] = df['genre'].astype(str)
        
        id_list = recommend_songs(song_id=song_id,data=df)
        
        return SuccessResponse(data = await self.db.get_songs(id_list=id_list) )
    
