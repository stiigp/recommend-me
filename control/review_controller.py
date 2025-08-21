import logging

from model.review import Review
from model.movie import Movie
from model.user import User
from db.entities.movie_model import MovieModel
from db.entities.user_model import UserModel
from fastapi import HTTPException
from schemas.review_dto import ReviewDTO
from sqlalchemy.orm import Session

logger = logging.getLogger("uvicorn.error")

class ReviewController:
    def __init__(self, payload: ReviewDTO=None, session:Session=None):
        self.payload = payload
        self.session = session

    def save(self):
        try:
            review = Review(
                rating=self.payload.rating,
                description=self.payload.description,
                movie = Movie(
                    id=self.payload.movie_id
                ),
                user = User(
                    id=self.payload.user_id
                )
            )

            retorno = review.save(session=self.session)

            return {'message': 'review created successfully', 'review': retorno}
        except:
            raise

    def select(self):
        try:
            if self.payload != None:
                review = Review(user=User(
                    id=self.payload.user_id
                ))
            else:
                review = Review()
            
            reviews = review.list(session=self.session)

            return reviews
        except:
            raise
    
    def remove(self):
        review = Review(
            id=self.payload
        )

        try:
            review.delete(self.session)

            return {'message': f'review deleted successfully', 'id': self.payload}
        except:
            raise
    
    def update(self):
        try:
            review = Review(
                id=self.payload.id,
                rating=self.payload.rating,
                description=self.payload.description
            )

            res = review.update(self.session)

            return {'message': f'review updated successfully', 'review': res}
        except:
            raise
