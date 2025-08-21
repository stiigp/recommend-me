from db.entities.follow_model import FollowModel
from db.entities.user_model import UserModel
from model.user import User
from sqlalchemy.orm import Session, selectinload, load_only
from sqlalchemy import select, delete, update, and_
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

class Follow:
    def __init__(self, id: int=0, source:User=None, dest:User=None):
        self.id = id
        self.source = source
        self.dest = dest

    def save(self, session: Session):
        follow_model = FollowModel(
            source_id=self.source.id,
            dest_id=self.dest.id
        )

        try:
            session.add(follow_model)
            session.commit()
            session.refresh(follow_model)

            return follow_model
        
        except Exception as e:
            session.rollback()
            if isinstance(e, IntegrityError):
                err = HTTPException(
                    status_code=404,
                    detail=f'integrity error (probably source or dest doesnt exist): {str(e.orig).lower()}'
                )
                raise err
            
            raise e

    def list(self, session:Session):
        if self.source == None and self.dest == None:
            stmt = select(FollowModel).options(
                selectinload(
                    FollowModel.source
                ).options(
                    load_only(UserModel.id, UserModel.username)
                ),
                selectinload(
                    FollowModel.dest
                ).options(
                    load_only(UserModel.id, UserModel.username)
                )
            )
        elif self.dest == None:
            stmt = select(FollowModel).where(
                FollowModel.source_id == self.source.id
            ).options(
                selectinload(
                    FollowModel.source
                ).options(
                    load_only(UserModel.id, UserModel.username)
                ),
                selectinload(
                    FollowModel.dest
                ).options(
                    load_only(UserModel.id, UserModel.username)
                )
            )
        else:
            stmt = select(FollowModel).where(
                FollowModel.dest_id == self.dest.id
            ).options(
                selectinload(
                    FollowModel.source
                ).options(
                    load_only(UserModel.id, UserModel.username)
                ),
                selectinload(
                    FollowModel.dest
                ).options(
                    load_only(UserModel.id, UserModel.username)
                )
            )
        
        try:
            follows = session.execute(
                stmt
            ).scalars().all()

            
            return follows
        except:
            raise
    
    def delete(self, session: Session):
        try:
            stmt = (
                delete(FollowModel)
                .where(
                    and_(
                        FollowModel.source_id == self.source.id,
                        FollowModel.dest_id == self.dest.id
                    )
                )
                .returning(FollowModel.source_id, FollowModel.dest_id)
            )

            result = session.execute(stmt).scalar()

            if result is None:
                raise HTTPException(
                    status_code=404,
                    detail="trying to delete non-existent follow"
                )
            
            session.commit()

            return result
        
        except:
            session.rollback()

            raise

