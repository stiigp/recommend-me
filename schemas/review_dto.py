from pydantic import BaseModel
from typing import Optional

class ReviewDTO(BaseModel):
    rating:Optional[float]=None
    description:Optional[str]=None
    movie_id:Optional[int]=None
    user_id:Optional[int]=None
