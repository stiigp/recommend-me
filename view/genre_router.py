from fastapi import APIRouter
from schemas.genre_dto import GenreDTO
from control.genre_controller import GenreController
from db.db import get_session

genre_router = APIRouter(
    prefix='/genres',
    tags=['genres']
)

@genre_router.get('/')
def list_genres():
    try:
        with get_session() as session:
            genre_ctrl = GenreController(session=session)

            return genre_ctrl.select()
    except:
        raise

@genre_router.post('/') 
def register_genre(genre: GenreDTO):
    try:
        with get_session() as session:
            genre_ctrl = GenreController(payload=genre, session=session)

            return genre_ctrl.save()
    except:
        raise

@genre_router.delete('/{id}')
def delete_genre(id: int):
    try:
        with get_session() as session:
            genre_ctrl = GenreController(payload=id, session=session)

            return genre_ctrl.remove()
    except:
        raise

@genre_router.patch('/{id}')
def update_genre(id: int, genre: GenreDTO):
    try:
        with get_session() as session:
            genre_ctrl = GenreController(payload={'id': id, 'genre': genre}, session=session)

            return genre_ctrl.update()
    except:
        raise
