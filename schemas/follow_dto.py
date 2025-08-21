from pydantic import BaseModel
from typing import Optional

class FollowDTO(BaseModel):
    source_id:Optional[int]=None
    dest_id:Optional[int]=None