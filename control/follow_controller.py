import logging

from model.follow import Follow
from model.user import User
from fastapi import HTTPException
from schemas.follow_dto import FollowDTO
from sqlalchemy.orm import Session

logger = logging.getLogger("uvicorn.error")

class FollowController:
    def __init__(self, payload: FollowDTO=None, session:Session=None):
        self.payload = payload
        self.session = session

    def save(self):
        try:
            follow = Follow(
                source=User(
                    id=self.payload.source_id
                ),
                dest=User(
                    id=self.payload.dest_id
                )
            )

            retorno = follow.save(session=self.session)

            return {'message': 'follow created succesfully', 'follow': retorno}
        
        except:
            raise

    def select(self):
        follow = Follow()

        if self.payload != None:
            if 'source_id' in self.payload:
                follow = Follow(
                    source=User(
                        id=self.payload['source_id']
                    )
                )
            elif 'dest_id' in self.payload:
                follow = Follow(
                    dest=User(
                        id=self.payload['dest_id']
                    )
                )

        try:
            follows = follow.list(self.session)

            return follows
        
        except:
            raise

    def remove(self):
        follow = Follow(
            source=User(
                id=self.payload.source_id
            ),
            dest=User(
                id=self.payload.dest_id
            )
        )

        try:
            follow.delete(self.session)

            return {'message': f'follow deleted successfully', 'id': self.payload}
        except:
            raise
