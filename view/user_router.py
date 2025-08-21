from fastapi import APIRouter
from schemas.user_dto import UserDTO
from control.user_controller import UserController
from db.db import get_session

user_router = APIRouter(
    prefix='/users',
    tags=['users']
)

@user_router.get('/')
def list_users():
    try:
        with get_session() as session:
            usr_ctrl = UserController(session=session)

            return usr_ctrl.select()
    except:
        raise

@user_router.post('/')
def register_user(user: UserDTO):
    try:
        with get_session() as session:
            usr_ctrl = UserController(payload = user, session=session)

            return usr_ctrl.save()
    except:
        raise
    
@user_router.delete('/{id}')
def delete_user(id: int):
    try:
        with get_session() as session:
            usr_ctrl = UserController(payload=id, session=session)

            return usr_ctrl.remove()
    except:
        raise

@user_router.patch('/{id}')
def update_user(id: int, user: UserDTO):
    user.id = id
    try:
        with get_session() as session:
            usr_ctrl = UserController(payload=user, session=session)
            
            return usr_ctrl.update()
    except:
        raise
    