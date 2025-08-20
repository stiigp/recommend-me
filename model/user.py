import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete, update
from db.entities.user_model import UserModel
from model.utils.hasher import Hasher
from schemas.user_dto import UserDTO
from fastapi import HTTPException

logger = logging.getLogger("uvicorn.error")

class User:
    def __init__(self, id: int=0, username: str="", password: str="", email: str=""):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
    
    def save(self, session: Session):
        hasher = Hasher(self.password)

        user_model = UserModel(
            username=self.username,
            email=self.email,
            password_hash = hasher.encrypt()
        )

        try:
            session.add(user_model)
            session.commit()
            session.refresh(user_model)

            del user_model.password_hash

            return user_model
        except:
            session.rollback()

            raise

    def list(self, session: Session):
        try:
            all_users = session.execute(select(UserModel.id, UserModel.username, UserModel.email, UserModel.created_at)).all()

            res = [{"id": user.id, "username": user.username, "email": user.email, "created_at": user.created_at} for user in all_users]

            return res
        except:
            raise

    def delete(self, session: Session):
        try:
            user = session.execute(select(UserModel).where(UserModel.id == self.id)).scalar()
            
            if user == None:
                raise HTTPException(
                    status_code=404,
                    detail="trying to delete non-existent user"
                )
            
            stmt = delete(UserModel).where(UserModel.id == self.id)
            
            session.execute(stmt)
            session.commit()

            return
        except:
            session.rollback()
            raise

    def update(self, session: Session):
        try:
            user = session.execute(select(UserModel).where(UserModel.id == self.id)).scalar()

            if user == None:
                raise HTTPException(
                    status_code=404,
                    detail="trying to alter non-existent user"
                )
            
            args = {}

            if self.username != None:
                args['username'] = self.username
            if self.email != None:
                args['email'] = self.email
            if self.password != None:
                hasher = Hasher(input=self.password)
                args['password_hash'] = hasher.encrypt()

            stmt = update(UserModel).where(UserModel.id == self.id).values(**args)
            
            session.execute(stmt)
            session.commit()

            user = session.execute(select(UserModel).where(UserModel.id == self.id)).scalar()
            del user.password_hash

            return user
            
        except:
            session.rollback()
            raise
