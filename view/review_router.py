from fastapi import APIRouter
from schemas.review_dto import ReviewDTO
from control.review_controller import ReviewController
from db.db import get_session

review_router = APIRouter(
    prefix='/reviews',
    tags=['reviews']
)

@review_router.post('/')
def register_review(review: ReviewDTO):
    try:
        with get_session() as session:
            rv_ctrl = ReviewController(payload=review, session=session)

            return rv_ctrl.save()
    except:
        raise

@review_router.get('/')
def list_reviews():
    try:
        with get_session() as session:
            rv_ctrl = ReviewController(session=session)

            return rv_ctrl.select()
    except:
        raise

@review_router.get('/{id}')
def list_reviews_user(id: int):
    try:
        with get_session() as session:
            rv_ctrl = ReviewController(payload=id, session=session)

            return rv_ctrl.select()
    except:
        raise

@review_router.delete('/{id}')
def delete_review(id: int):
    try:
        with get_session() as session:
            rv_ctrl = ReviewController(payload=id, session=session)

            return rv_ctrl.remove()
    except:
        raise

@review_router.patch('/{id}')
def update_user(id: int, review: ReviewDTO):
    try:
        with get_session() as session:
            rv_ctrl = ReviewController(payload={'id': id, 'review': review}, session=session)

            return rv_ctrl.update()
    except:
        raise
