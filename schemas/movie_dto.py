from pydantic import BaseModel
from typing import Optional

class MovieDTO(BaseModel):
    id: Optional[int]=None
    title:Optional[str]=None
    year:Optional[int]=None
    genre_id:Optional[int]=None
