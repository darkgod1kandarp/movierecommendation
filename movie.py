from typing import List
import numpy as np 
import pandas as pd 
import difflib 
from sklearn.feature_extraction.text import TfidfVectorizer  
from sklearn.metrics.pairwise import cosine_similarity



def similarity_matrix():
    """
    Takes No Input 

    Returns:
        [type]: [array]
    """

    movies_data  =  pd.read_csv("movies.csv")
    selected_feature  =  ['genres' ,  'keywords' ,  'tagline' , 'cast' , 'director' ]


    for feature  in selected_feature:
        movies_data[feature] = movies_data[feature].fillna('')


    combined_feature  =  movies_data['genres'] + movies_data['keywords'] + movies_data['tagline'] + movies_data['cast']  + movies_data['director']
    vectorizer  =  TfidfVectorizer()
    feature_vectors  =  vectorizer.fit_transform(combined_feature)

    similarity  =  cosine_similarity(feature_vectors)


    return similarity ,  movies_data['title'], movies_data


def main_func(movie_name:str ,  list_of_movies , movies_data , similarity:List[List[float]] , recommended_movies:List[str]):
    find_close_match  =  difflib.get_close_matches(movie_name   , list_of_movies)
    if find_close_match:

        close_match = find_close_match[0]
        index_of_the_movie  =   movies_data[movies_data.title ==close_match]['index'].values[0]
        similarity_score  = list(enumerate(similarity[index_of_the_movie]))
        sorted_similar_movies  =  sorted(similarity_score , key  =  lambda  x  :   x[1] , reverse  = True ) 
        
        for movie in sorted_similar_movies[:5]:
            index  =  movie[0]
            title_from_index  =  movies_data[movies_data.index==index]['title'].values[0]
          
            recommended_movies.append(title_from_index)

