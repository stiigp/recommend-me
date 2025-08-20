from db.entities.like_model import LikeModel
from model.review import Review
from model.user import User
from sqlalchemy.orm import Session, selectinload, load_only
from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

class Like:
    def __init__(self, id: int=0, user:User=None, review:Review=None):
        self.id = id
        self.user = user
        self.review = review

    def save(self, session: Session):
        like_model = LikeModel(
            user_id=self.user.id,
            review_id=self.review.id
        )

        try:
            session.add(like_model)
            session.commit()
            session.refresh(like_model)

            return like_model
        
        except Exception as e:
            session.rollback()
            if isinstance(e, IntegrityError):
                err = HTTPException(
                    status_code=404,
                    detail=f'integrity error (probably review or user doesnt exist): {str(e.orig).lower()}'
                )
                raise err
            
            raise e
    
    def list(self, session:Session):
        if self.user == None and self.review == None:
            stmt = select(LikeModel)
        elif self.review == None:
            stmt = select(LikeModel).where(
                LikeModel.user_id == self.user.id
            )
        else:
            stmt = select(LikeModel).where(
                LikeModel.review_id == self.review.id
            )
        
        try:
            likes = session.execute(
                stmt
            ).scalars().all()

            return likes
        except:
            raise
    
    def delete(self, session: Session):
        try:
            stmt = delete(LikeModel).where(LikeModel.id == self.id).returning(LikeModel.id)

            result = session.execute(stmt).scalar()

            if result is None:
                raise HTTPException(
                    status_code=404,
                    detail="trying to delete non-existent like"
                )
            
            session.commit()

            return result
            
        except:
            session.rollback()

            raise
