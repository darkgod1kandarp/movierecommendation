
from ast import Str
from typing import List
import uvicorn
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from movie import similarity_matrix, main_func
import os

import random

similarity,  list_of_movies, movies_data = similarity_matrix()


@strawberry.type
class Query:
    @strawberry.field
    def search_bar(self, movie_name: str) -> List[str]:
        recommended_movies = []
        main_func(movie_name,  list_of_movies, movies_data,
                  similarity, recommended_movies)
        return recommended_movies

    @strawberry.field
    async def movie_recommendation(self, last_movies: List[str]) -> List[str]:
        recommended_movies = []

        for movie_name in last_movies:
            main_func(movie_name,  list_of_movies, movies_data,
                      similarity, recommended_movies)

        random.seed(0)
        random.shuffle(recommended_movies)
        return recommended_movies


schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(schema)
app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=2)
