import json
import numpy as np
import pandas as pd
from bson import ObjectId
from db.redis.init import RedisDB
from fastapi import BackgroundTasks
from Services.DBService import DBService
from sklearn.ensemble  import RandomForestClassifier
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

class RecommendationService:
    def __init__(self) -> None:
        self.db_service = DBService()
        self.cache =  RedisDB.getInstance()
    
    #Private class    
    def __get_similarities(self,song_id:str, data:pd.DataFrame)->list:
        
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
            
            
        
        
    #Private class      
    def __GetSimilarSongs(self,song_id:str, data:pd.DataFrame)-> list:
        
        data['similarity_factor'] = self.__get_similarities(song_id, data)
        data.sort_values(by='similarity_factor',ascending = False,inplace=True)
        data = data.drop(data[data['_id'] == song_id].index)
        
        return data['_id'].head(12).values.tolist()
        
        
    
    
    async def Recommend_Similarities(self,song_id:str)->list:
        
        df = await self.db_service.GetSongsStats(song_id)
        if df.shape[0] == 0 : 
            return await self.db_service.GetSongs(exclude_id=song_id) 
        
        id_list = self.__GetSimilarSongs(song_id=song_id,data=df)
        
        return await self.db_service.GetSongs(id_list=id_list)
        
    #Private class  
    def __BuildRandomForest(self,songStats:list,listen_counts:dict)->RandomForestClassifier | None:
        
        userRecord = pd.DataFrame(songStats)
        userRecord['reaction'] = 0
        
        for index , row in userRecord.iterrows():
            userRecord.iloc[index,-1] = 1 if listen_counts[str(row['_id'])] >=2 else 0
        
        userRecord = userRecord.drop(['_id','mode','duration_ms','time_signature','genre'],axis=1)
        x_train = userRecord.values[:,:-1]
        y_train = userRecord.values[:,-1]
        clf = RandomForestClassifier(n_estimators=4,max_features=None,random_state=42,max_depth=3,bootstrap=True)
        
        return clf.fit(x_train,y_train)
        
        
        
    #Private class      
    async def __CreateNewRecommendation(self,user_id:str | None,model:RandomForestClassifier,id_list:list)->bool:
        
        records:list = await self.db_service.GetAllSongsStats(id_list)
        recommend_ids:list[str] = []
        
        record:dict
        for record in records:
            _id:ObjectId = record.pop('_id')
            positive:bool = model.predict(np.array(list(record.values())).reshape(1, -1)) > 0
            if positive : recommend_ids.append(str(_id))
        
        recommend_data:dict = {
            'read_count':0,
            'ids':recommend_ids
        }
               
        if recommend_ids : 
            return await self.cache.set(user_id,json.dumps(recommend_data)) is not None
            
        return False     
        
    #Private class      
    async def __GenerateNewSongsRecommendation(self,user_id:str | None,userItem:dict):
        
        records:list = userItem['records']
        songStats:list = userItem['Songs-Stats']
        listen_counts = {}
        count = 0
        
        for r in records:
            listen_counts[str(r['song_id'])] = r['user_listen_counts']
            if r['user_listen_counts'] >=2: count+=1
        
        if count < 2 : return False
        
        model = self.__BuildRandomForest(songStats,listen_counts)
        ids = []
        
        id:str
        for id in listen_counts.keys():
            ids.append(ObjectId(id))
        
        acknowledge:bool = await self.__CreateNewRecommendation(user_id,model,ids)
        
        return acknowledge
    
    async def Recommend_NewSongs(self,user_id:str|None , b_tasks: BackgroundTasks)->list | None:
      
        if user_id is None : return None
         
        result:list = await self.db_service.GetUserItemsRecord(user_id)
        userItem:dict | None  = result[0]
        
        if userItem is None : return []
        #Create background task so the client wont have to wait until the model finish recommending new songs
        
        recommend_data:str = await self.cache.get(user_id)
        if not recommend_data : 
            b_tasks.add_task(self.__GenerateNewSongsRecommendation,user_id,userItem)
            return None 
        
        data:dict = json.loads(recommend_data)
        read_count:int = data['read_count']
        id_list :list = data['ids']
        
        if read_count > 10:
            b_tasks.add_task(self.__GenerateNewSongsRecommendation,user_id,userItem)
        
        else : 
            data['read_count']+=1
            await self.cache.set(user_id,json.dumps(data))
            
            
        ids = []
        
        for id in id_list: 
            ids.append(ObjectId(id))
        
        return await self.db_service.GetSongs(ids) 
    
        
        

        
        

            
            

        
        
        
        
    
    