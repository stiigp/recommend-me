from db.entities.movie_model import MovieModel
from model.genre import Genre
from sqlalchemy.orm import Session, selectinload, load_only
from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError
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
            main_genre=self.genre.id
        )

        try:
            session.add(movie_model)
            session.commit()
            session.refresh(movie_model, ["genre"])

            return movie_model
        except Exception as e:
            session.rollback()
            if isinstance(e, IntegrityError):
                err = HTTPException(
                    status_code=404,
                    detail=f"integrity error (probably genre doenst exist): {str(e.orig).lower()}"
                )
                raise err

            raise e
    
    def list(self, session: Session):
        try:
            all_movies = session.execute(select(MovieModel).options(
                selectinload(MovieModel.genre),
                load_only(
                    MovieModel.id,
                    MovieModel.title,
                    MovieModel.year
                )
            )).scalars().all()

            return all_movies
        except:
            raise
    
    def delete(self, session: Session):
        try:
            stmt = delete(MovieModel).where(MovieModel.id == self.id).returning(MovieModel.id)

            movie = session.execute(stmt).scalar()

            if movie is None:
                raise HTTPException(
                    status_code=404,
                    detail="trying to delete non-existent movie"
                )

            session.commit()

            return
        except:
            session.rollback()
            raise

    def update(self, session: Session):
        try:
            movie = session.get(MovieModel, self.id)

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
            if self.genre.id != None:
                args['main_genre'] = self.genre.id
            
            stmt = update(MovieModel).where(MovieModel.id == self.id).values(**args)

            session.execute(stmt)
            session.commit()

            session.refresh(movie, ['genre'])

            return movie
        
        except Exception as e:
            session.rollback()

            if isinstance(e, IntegrityError):
                err = HTTPException(
                    status_code=404,
                    detail=f'integrity error (probably genre youre trying to alter to doesnt exist): {str(e.orig).lower()}'
                )

                raise err

            raise e
