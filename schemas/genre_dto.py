from pydantic import BaseModel
from typing import Optional

class GenreDTO(BaseModel):
    id: Optional[int]=None
    name: Optional[str] = None
