from db.db import Base
from db.entities.review_model import ReviewModel
from db.entities.user_model import UserModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, func, CheckConstraint
from datetime import datetime

class FollowModel(Base):
    __tablename__ = "follows"

    source_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    dest_id   = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    source = relationship(
        "UserModel",
        foreign_keys=[source_id],
        back_populates="following_assocs"
    )
    dest = relationship(
        "UserModel",
        foreign_keys=[dest_id],
        back_populates="followers_assocs"
    )
    
    __table_args__ = (
        CheckConstraint("source_id <> dest_id", name="check_source_dest_diff"),
    )
