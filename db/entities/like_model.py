from db.db import Base
from db.entities.review_model import ReviewModel
from db.entities.user_model import UserModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from datetime import datetime

class LikeModel(Base):
    __tablename__ = 'likes'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    review_id: Mapped[int] = mapped_column(ForeignKey('reviews.id', ondelete="CASCADE"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user: Mapped["UserModel"] = relationship()
    review: Mapped["ReviewModel"] = relationship()
