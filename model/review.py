import logging

from model.user import User
from model.movie import Movie
from sqlalchemy.orm import Session, selectinload, load_only
from db.entities.review_model import ReviewModel
from db.entities.user_model import UserModel
from db.entities.movie_model import MovieModel
from sqlalchemy import select, update, delete
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
            user=self.user,
            movie=self.movie,
            rating=self.rating,
            description=self.description
        )

        try:
            session.add(review_model)
            session.commit()
            session.refresh(review_model)

            return review_model
        except:
            session.rollback()

            raise

    def list(self, session: Session):
        if self.user != None:
            stmt = (
                select(ReviewModel)
                .options(
                    selectinload(ReviewModel.user).options(
                        load_only(UserModel.id, UserModel.username)
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
            ).where(ReviewModel.id == self.id)
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
            reviews = session.execute(stmt).scalars().all()

            return reviews
        except:
            raise

    def delete(self, session: Session):
        stmt = select(ReviewModel).where(ReviewModel.id == self.id)
        try:
            review = session.execute(stmt)

            if review == None:
                raise HTTPException(
                    status_code=404,
                    detail="trying to delete non-existent review"
                )
            
            stmt = delete(ReviewModel).where(ReviewModel.id == self.id)

            session.execute(stmt)
            session.commit()

            return
        except:
            session.rollback()

            raise

    def update(self, session: Session):
        stmt = select(ReviewModel).where(ReviewModel.id == self.id)
        try:
            review = session.execute(stmt)

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
