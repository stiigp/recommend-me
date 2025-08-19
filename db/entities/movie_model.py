from db.db import Base
from db.entities.genre_model import GenreModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey

class MovieModel(Base):
    __tablename__ = 'movies'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    year: Mapped[int] = mapped_column(Integer)
    main_genre:Mapped[int] = mapped_column(ForeignKey('genres.id'))
    genre: Mapped["GenreModel"] = relationship()