import logging

from model.review import Review
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
            movie = self.session.get(MovieModel, self.payload.movie_id)

            if movie == None:
                raise HTTPException(
                    status_code=404,
                    detail='movie corresponding to the review doesnt exist'
                )
            
            user = self.session.get(UserModel, self.payload.user_id)

            if user == None:
                raise HTTPException(
                    status_code=404,
                    detail='user corresponding to the review doesnt exist'
                )
            
            review = Review(
                rating=self.payload.rating,
                description=self.payload.description,
                movie = movie,
                user = user
            )

            retorno = review.save(session=self.session)

            return {'message': 'review created successfully', 'review': retorno}
        except:
            raise

    def select(self):
        try:
            if isinstance(self.payload, int):
                user = self.session.get(UserModel, self.payload)

                if user == None:
                    raise HTTPException(
                        status_code=404,
                        detail='user doesnt exist!'
                    )
                
                review = Review(user=user)

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
                id=self.payload['id'],
                rating=self.payload['review'].rating,
                description=self.payload['review'].description
            )

            res = review.update(self.session)

            return {'message': f'review updated successfully', 'review': res}
        except:
            raise
