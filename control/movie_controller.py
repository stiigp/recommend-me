import logging

from model.movie import Movie
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
            genre = self.session.get(GenreModel, self.payload.genre_id)

            if genre == None:
                raise HTTPException(
                    status_code=404,
                    detail='genre corresponding to the movie doenst exist'
                )

            movie = Movie(
                title=self.payload.title,
                year=self.payload.year,
                genre=genre
            )

            retorno = movie.save(session=self.session)

            retorno.main_genre = {
                'id': genre.id,
                'name': genre.name
            }

            return {'message': 'movie created succesfully', 'movie': retorno}
        except:
            raise
    
    def select(self):
        movie = Movie()

        try:
            all_movies = movie.list(session=self.session)

            all_movies = [
                {
                    'id': iMovie['id'],
                    'title': iMovie['title'],
                    'year': iMovie['year'],
                    'genre': self.session.get(GenreModel, iMovie['main_genre'])
                }
                for iMovie in all_movies
            ]

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
            genre = None
            if self.payload['movie'].genre_id != None:
                genre = self.session.get(GenreModel, self.payload['movie'].genre_id)

                if genre == None:
                    raise HTTPException(
                        status_code=404,
                        detail='genre corresponding to the movie doenst exist'
                    )

            if genre == None:
                movie = Movie(
                    id=self.payload['id'],
                    title=self.payload['movie'].title,
                    year=self.payload['movie'].year
                )
            else:
                movie = Movie(
                    id=self.payload['id'],
                    title=self.payload['movie'].title,
                    year=self.payload['movie'].year,
                    genre=genre
                )

            res = movie.update(self.session)

            if genre == None:
                genre = self.session.get(GenreModel, res.main_genre)

            res.main_genre = {
                'id': genre.id,
                'name': genre.name
            }

            return {'message': f'movie updated successfully', 'movie': res}
        except:
            raise