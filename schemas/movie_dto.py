from pydantic import BaseModel
from typing import Optional

class MovieDTO(BaseModel):
    title:Optional[str]=None
    year:Optional[int]=None
    genre_id:Optional[int]=None
