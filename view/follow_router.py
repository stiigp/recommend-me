from fastapi import APIRouter
from schemas.follow_dto import FollowDTO
from control.follow_controller import FollowController
from db.db import get_session

follow_router = APIRouter(
    prefix='/follows',
    tags=['follows']
)

@follow_router.post('/')
def register_follow(follow: FollowDTO):
    try:
        with get_session() as session:
            fl_ctrl = FollowController(payload=follow, session=session)

            return fl_ctrl.save()
    except:
        raise

@follow_router.get('/')
def list_follows():
    try:
        with get_session() as session:
            fl_ctrl = FollowController(session=session)

            return fl_ctrl.select()
    except:
        raise

@follow_router.get('/sources/{id}')
def list_follows_source(id: int):
    try:
        with get_session() as session:
            fl_ctrl = FollowController(payload={'source_id': id}, session=session)

            return fl_ctrl.select()
    except:
        raise

@follow_router.get('/dests/{id}')
def list_follows_dest(id: int):
    try:
        with get_session() as session:
            fl_ctrl = FollowController(payload={'dest_id': id}, session=session)

            return fl_ctrl.select()
    except:
        raise

@follow_router.delete('/{source_id}/{dest_id}')
def delete_follow(source_id: int, dest_id:int):
    try:
        with get_session() as session:
            fl_ctrl = FollowController(payload=FollowDTO(
                source_id=source_id,
                dest_id=dest_id
            ), session=session)

            return fl_ctrl.remove()
    except:
        raise
