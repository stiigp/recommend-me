import logging

from model.movie import Movie
from model.genre import Genre
from db.entities.genre_model import GenreModel
from fastapi import HTTPException
from schemas.movie_dto import MovieDTO
from sqlalchemy.orm import Session

logger = logging.getLogger("uvicorn.error")

class MovieController:
    def __init__(self, payload: MovieDTO=None, session:Session=None):
        self.payload = payload
        self.session = session

    def save(self):
        try:            
            movie = Movie(
                title=self.payload.title,
                year=self.payload.year,
                genre=Genre(
                    id=self.payload.genre_id
                )
            )

            retorno = movie.save(session=self.session)

            return {'message': 'movie created succesfully', 'movie': retorno}
        except:
            raise
    
    def select(self):
        movie = Movie()

        try:
            all_movies = movie.list(session=self.session)

            return all_movies
        except:
            raise
    
    def remove(self):
        movie = Movie(
            id=self.payload
        )

        try:
            movie.delete(self.session)

            return {'message': f'movie deleted successfully', 'id': self.payload}
        except:
            raise

    def update(self):
        try:                        
            movie = Movie(
                id=self.payload.id,
                title=self.payload.title,
                year=self.payload.year,
                genre=Genre(
                    id=self.payload.genre_id
                )
            )

            res = movie.update(self.session)

            return {'message': f'movie updated successfully', 'movie': res}
        except:
            raise