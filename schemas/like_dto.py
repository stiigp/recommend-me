from pydantic import BaseModel
from typing import Optional

class LikeDTO(BaseModel):
    user_id:Optional[int]=None
    review_id:Optional[int]=None