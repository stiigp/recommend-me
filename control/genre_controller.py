from schemas.genre_dto import GenreDTO
from sqlalchemy.orm import Session
from model.genre import Genre

class GenreController:
    def __init__(self, payload: GenreDTO=None, session: Session=None):
        self.payload = payload
        self.session = session

    def save(self):
        genre = Genre(
            name=self.payload.name
        )

        try:
            retorno = genre.save(session=self.session)

            return {"message": "genre created successfully", "genre": retorno}
        except:
            raise
    
    def select(self):
        genre = Genre()

        try:
            return genre.list(session=self.session)
        except:
            raise

    def remove(self):
        genre = Genre(
            id=self.payload
        )

        try:
            genre.delete(self.session)

            return {'message': f'genre deleted successfully', 'id': self.payload}
        except:
            raise
    
    def update(self):
        genre = Genre(
            id=self.payload['id'],
            name = self.payload['genre'].name
        )

        try:
            res = genre.update(self.session)

            return {'message': f'genre updated successfully', 'genre': res}
        except:
            raise
