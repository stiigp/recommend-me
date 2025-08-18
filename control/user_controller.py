from schemas.user_dto import UserDTO
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from model.user import User

class UserController:
    def __init__(self, payload: UserDTO=None, session: Session=None):
        self.payload = payload
        self.session = session

    def save(self):
        user = User(
            username=self.payload.username,
            email=self.payload.email,
            password=self.payload.password
        )

        try:
            retorno = user.save(session=self.session)

            return {"message": "user created succesfully", "user": retorno}
        except:
            raise
        
    def select(self):
        user = User()

        try:
            return user.list(session=self.session)
        except:
            raise

    def remove(self):
        user = User(
            id=self.payload
        )

        try:
            user.delete(self.session)

            return {'message': f'user deleted successfully', 'id': self.payload}
        except:
            raise

    def update(self):
        user = User(
            id=self.payload['id'],
            username = self.payload['user'].username,
            password=self.payload['user'].password,
            email=self.payload['user'].email
        )

        try:
            res = user.update(self.session)

            return {'message': f'user updated successfully', 'user': res}
        except:
            raise