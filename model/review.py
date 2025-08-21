import logging

from model.user import User
from model.movie import Movie
from sqlalchemy.orm import Session, selectinload, load_only
from db.entities.review_model import ReviewModel
from db.entities.user_model import UserModel
from db.entities.movie_model import MovieModel
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

logger = logging.getLogger("uvicorn.error")

class Review:
    def __init__(self, id: int=0, user: User=None, movie:Movie=None, rating:float=0.0, description:str=""):
        self.id = id
        self.user = user
        self.movie = movie
        self.rating = rating
        self.description = description
    
    def save(self, session: Session):
        review_model = ReviewModel(
            user_id=self.user.id,
            movie_id=self.movie.id,
            rating=self.rating,
            description=self.description
        )

        try:
            session.add(review_model)
            session.commit()
            session.refresh(review_model, ['user', 'movie'])

            del review_model.user.password_hash

            return review_model
        except Exception as e:
            session.rollback()

            if isinstance(e, IntegrityError):
                err = HTTPException(
                    status_code=404,
                    detail=f'integrity error (probably user or movie doesnt exist): {str(e.orig).lower()}'
                )

                raise err

            raise e

    def list(self, session: Session):
        if self.user != None:
            user_db = session.get(UserModel, self.user.id)

            if user_db is None:
                err = HTTPException(
                    status_code=404,
                    detail=f'user doesnt exist'
                )

                raise err

            stmt = (
                select(ReviewModel)
                .options(
                    selectinload(ReviewModel.user).options(
                        load_only(UserModel.username)
                    ),
                    selectinload(ReviewModel.movie).options(
                        load_only(MovieModel.id, MovieModel.title)
                    ),
                    load_only(
                        ReviewModel.id,
                        ReviewModel.rating,
                        ReviewModel.description
                    )
                )
            ).where(ReviewModel.user_id == self.user.id)
        else:
            stmt = (
                select(ReviewModel)
                .options(
                    selectinload(ReviewModel.movie).options(
                        load_only(MovieModel.id, MovieModel.title)
                    ),
                    selectinload(ReviewModel.user).options(
                        load_only(UserModel.id, UserModel.username)
                    ),
                    load_only(
                        ReviewModel.id,
                        ReviewModel.rating,
                        ReviewModel.description
                    )
                )
            )

        try:
            session.expunge_all()
            reviews = session.execute(stmt).scalars().all()

            return reviews
        except:
            raise

    def delete(self, session: Session):
        try:
            stmt = delete(ReviewModel).where(ReviewModel.id == self.id).returning(ReviewModel.id)

            res = session.execute(stmt).scalar()

            if res is None:
                raise HTTPException(
                    status_code=404,
                    detail="trying to delete non-existent review"
                )
            
            session.commit()

            return
        except:
            session.rollback()

            raise

    def update(self, session: Session):
        try:
            review = session.get(ReviewModel, self.id)

            if review == None:
                raise HTTPException(
                    status_code=404,
                    detail="trying to alter non-existent review"
                )
            
            args = {}

            if self.description != None:
                args['description'] = self.description
            if self.rating != None:
                args['rating'] = self.rating
            
            stmt = update(ReviewModel).where(ReviewModel.id == self.id).values(**args)

            session.execute(stmt)
            session.commit()

            review = session.execute(select(ReviewModel).where(ReviewModel.id == self.id)).scalar()

            return review
        except:
            session.rollback()

            raise
