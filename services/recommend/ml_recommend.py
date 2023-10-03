import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
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
        
        id_list = self.recommend_songs(song_id=song_id,data=df)
        
        return SuccessResponse(data = await self.db.get_songs(id_list=id_list) )
    
    def get_similarities(self,song_id, data):
        
        song_vectorizer = CountVectorizer()
        
        song_vectorizer.fit(data['genre'])
        
        text_array1 = song_vectorizer.transform(data[data['_id']==song_id]['genre']).toarray()
        
        num_array1 = data[data['_id']==song_id].select_dtypes(include=np.number).to_numpy()

        sim = []
        
        for idx, row in data.iterrows():
            
            index = row['_id']
            
            text_array2 = song_vectorizer.transform(data[data['_id']==index]['genre']).toarray()
            
            num_array2 = data[data['_id']==index].select_dtypes(include=np.number).to_numpy()

            text_sim = cosine_similarity(text_array1, text_array2)[0][0]
            
            num_sim = cosine_similarity(num_array1, num_array2)[0][0]
            
            sim.append(text_sim + num_sim)

        return sim

    def recommend_songs(self,song_id, data):
        
        data['similarity_factor'] = self.get_similarities(song_id, data)
        
        data.sort_values(by='similarity_factor',ascending = False,inplace=True)
        
        data = data.drop(data[data['_id'] == song_id].index)
        
        return data['_id'].head(12).values.tolist()