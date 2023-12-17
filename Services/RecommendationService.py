from Services.MongodbService import DBService
from utils.Model_ReccommendSongs import recommend_songs

class ML_Model:
    def __init__(self) -> None:
        self.db = DBService()
        
    
    async def recommend(self,song_id:str)->list:
        
        df = await self.db.get_songsStats(song_id)
        
        if df.shape[0] == 0 : return await self.db.get_songs(exclude_id=song_id) 
        
        id_list = recommend_songs(song_id=song_id,data=df)
        
        return await self.db.get_songs(id_list=id_list)