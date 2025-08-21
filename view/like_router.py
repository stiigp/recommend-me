from fastapi import APIRouter
from schemas.like_dto import LikeDTO
from control.like_controller import LikeController
from db.db import get_session

like_router = APIRouter(
    prefix='/likes',
    tags=['likes']
)

@like_router.post('/')
def register_like(like: LikeDTO):
    try:
        with get_session() as session:
            lk_ctrl = LikeController(payload=like, session=session)

            return lk_ctrl.save()
    except:
        raise

@like_router.get('/')
def list_likes():
    try:
        with get_session() as session:
            lk_ctrl = LikeController(session=session)

            return lk_ctrl.select()
    except:
        raise

@like_router.get('/users/{id}')
def list_likes_user(id: int):
    try:
        with get_session() as session:
            lk_ctrl = LikeController(payload={'user_id': id}, session=session)

            return lk_ctrl.select()
    except:
        raise

@like_router.get('/reviews/{id}')
def list_likes_review(id: int):
    try:
        with get_session() as session:
            lk_ctrl = LikeController(payload={'review_id': id}, session=session)

            return lk_ctrl.select()
    except:
        raise

@like_router.delete('/{userId}/{reviewId}')
def delete_like(userId: int, reviewId: int):
    like = LikeDTO(
        user_id=userId,
        review_id=reviewId
    )
    
    try:
        with get_session() as session:
            lk_ctrl = LikeController(payload=like, session=session)

            return lk_ctrl.remove()
    except:
        raise
