import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def get_similarities(song_id, data):
        
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