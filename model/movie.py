from db.entities.movie_model import MovieModel
from model.genre import Genre
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update
from fastapi import HTTPException

class Movie:
    def __init__(self, id:int=0, title:str="", year:int=0, genre:Genre=None):
        self.id = id
        self.title = title
        self.year = year
        self.genre = genre

    def save(self, session:Session):
        movie_model = MovieModel(
            title=self.title,
            year=self.year,
            genre=self.genre
        )

        try:
            session.add(movie_model)
            session.commit()
            session.refresh(movie_model)

            return movie_model
        except:
            session.rollback()

            raise
    
    def list(self, session: Session):
        try:
            all_movies = session.execute(select(MovieModel.id, MovieModel.title, MovieModel.year, MovieModel.main_genre))

            res = [
                {
                    'id': movie.id,
                    'title': movie.title,
                    'year': movie.year,
                    'main_genre': movie.main_genre
                }
                for movie in all_movies
            ]

            return res
        except:
            raise
    
    def delete(self, session: Session):
        try:
            movie = session.execute(select(MovieModel).where(MovieModel.id == self.id)).scalar()

            if movie == None:
                raise HTTPException(
                    status_code=404,
                    detail="trying to delete non-existent movie"
                )
            
            stmt = delete(MovieModel).where(MovieModel.id == self.id)

            session.execute(stmt)
            session.commit()

            return
        except:
            session.rollback()
            raise

    def update(self, session: Session):
        try:
            movie = session.execute(select(MovieModel).where(MovieModel.id == self.id)).scalar()

            if movie == None:
                raise HTTPException(
                    status_code=404,
                    detail="trying to alter non-existent movie"
                )
            
            args = {}

            if self.title != None:
                args['title'] = self.title
            if self.year != None:
                args['year'] = self.year
            if self.genre != None:
                args['main_genre'] = self.genre.id
            
            stmt = update(MovieModel).where(MovieModel.id == self.id).values(**args)

            session.execute(stmt)
            session.commit()

            movie = session.execute(select(MovieModel).where(MovieModel.id == self.id)).scalar()

            return movie
        
        except:
            session.rollback()

            raise
