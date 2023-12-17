from utils.Model_GetSimilarities import get_similarities

def recommend_songs(song_id, data):
        
        data['similarity_factor'] = get_similarities(song_id, data)
        
        data.sort_values(by='similarity_factor',ascending = False,inplace=True)
        
        data = data.drop(data[data['_id'] == song_id].index)
        
        return data['_id'].head(12).values.tolist()