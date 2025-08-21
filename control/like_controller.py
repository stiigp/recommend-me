import logging

from model.like import Like
from model.user import User
from model.review import Review
from db.entities.review_model import ReviewModel
from db.entities.user_model import UserModel
from fastapi import HTTPException
from schemas.like_dto import LikeDTO
from sqlalchemy.orm import Session

logger = logging.getLogger("uvicorn.error")

class LikeController:
    def __init__(self, payload: LikeDTO=None, session:Session=None):
        self.payload = payload
        self.session = session

    def save(self):
        try:
            like = Like(
                user=User(id=self.payload.user_id),
                review=Review(id=self.payload.review_id)
            )

            retorno = like.save(session=self.session)

            return {'message': 'like created succesfully', 'like': retorno}
        except:
            raise
    
    def select(self):
        like = Like()

        if self.payload != None:
            if 'user_id' in self.payload:
                like = Like(
                    user=User(
                        id=self.payload['user_id']
                    )
                )
            elif 'review_id' in self.payload:
                like = Like(    
                    review=Review(
                        id=self.payload['review_id']
                    )
                )
        
        try:
            likes = like.list(session=self.session)

            return likes
        except:
            raise

    def remove(self):
        like = Like(
            user=User(
                id=self.payload.user_id
            ),
            review=Review(
                id=self.payload.review_id
            )
        )

        try:
            res = like.delete(self.session)

            return {'message': f'like deleted successfully', 'like': res}
        except:
            raise

