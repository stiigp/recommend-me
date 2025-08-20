from db.db import Base
from db.entities.genre_model import GenreModel
from db.entities.user_model import UserModel
from db.entities.movie_model import MovieModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Numeric, DateTime, func
from datetime import datetime

class ReviewModel(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    movie_id: Mapped[int] = mapped_column(ForeignKey('movies.id'))
    rating: Mapped[float] = mapped_column(Numeric(2, 1), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user: Mapped["UserModel"] = relationship()
    movie: Mapped["MovieModel"] = relationship()

    def __repr__(self) -> str:
        return f'Review(id={self.id!r}, userId={self.userId!r}, movieId={self.movieId!r}, rating={self.rating!r}, created_at={self.created_at!r})'
