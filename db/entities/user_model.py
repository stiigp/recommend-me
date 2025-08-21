from db.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, func
from datetime import datetime


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    following_assocs = relationship(
        "FollowModel",
        foreign_keys="FollowModel.source_id",
        back_populates="source",
        cascade="all, delete-orphan"
    )
    followers_assocs = relationship(
        "FollowModel",
        foreign_keys="FollowModel.dest_id",
        back_populates="dest",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, create_time={self.create_time!r})"
