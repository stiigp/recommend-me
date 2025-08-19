from db.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

class GenreModel(Base):
    __tablename__="genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
