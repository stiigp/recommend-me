from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update
from db.entities.genre_model import GenreModel
from fastapi import HTTPException

class Genre:
    def __init__(self, id: int=0, name:str=0):
        self.id = id
        self.name = name
    
    def save(self, session: Session):
        genre_model = GenreModel(
            name = self.name
        )

        try:
            session.add(genre_model)
            session.commit()
            session.refresh(genre_model)

            return genre_model
        
        except:
            session.rollback()

            raise

    def list(self, session: Session):
        try:
            all_genres = session.execute(select(GenreModel)).scalars().all()

            return all_genres
        except:
            raise
    
    def delete(self, session: Session):
        try:
            genre = session.execute(select(GenreModel).where(GenreModel.id == self.id)).scalar()

            if genre == None:
                raise HTTPException(
                    status_code=404,
                    detail="trying to delete non-existent genre"
                )
            
            stmt = delete(GenreModel).where(GenreModel.id == self.id)

            session.execute(stmt)
            session.commit()

            return
        except:
            session.rollback()

            raise

    def update(self, session: Session):
        try:
            genre = session.execute(select(GenreModel).where(GenreModel.id == self.id)).scalar()

            if genre == None:
                raise HTTPException(
                    status_code=404,
                    detail="trying to alter non-existent genre"
                )
            
            stmt = update(GenreModel).where(GenreModel.id == self.id).values(name=self.name)

            session.execute(stmt)
            session.commit()

            genre = session.execute(select(GenreModel).where(GenreModel.id == self.id)).scalar()

            return genre
        
        except:
            session.rollback()
            raise