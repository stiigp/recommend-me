from fastapi import APIRouter
from schemas.movie_dto import MovieDTO
from control.movie_controller import MovieController
from db.db import get_session

movie_router = APIRouter(
    prefix='/movies',
    tags=['movies']
)

@movie_router.post('/')
def register_movie(movie: MovieDTO):
    try:
        with get_session() as session:
            mv_ctrl = MovieController(payload=movie, session=session)

            return mv_ctrl.save()
    except:
        raise

@movie_router.get('/')
def list_users():
    try:
        with get_session() as session:
            mv_ctrl = MovieController(session=session)

            return mv_ctrl.select()
    except:
        raise

@movie_router.delete('/{id}')
def delete_user(id: int):
    try:
        with get_session() as session:
            mv_ctrl = MovieController(payload=id, session=session)

            return mv_ctrl.remove()
    except:
        raise

@movie_router.patch('/{id}')
def update_movie(id: int, movie: MovieDTO):
    try:
        with get_session() as session:
            mv_ctrl = MovieController(payload={'id': id, 'movie': movie}, session=session)

            return mv_ctrl.update()
    except:
        raise
