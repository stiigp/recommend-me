from pydantic import BaseModel
from typing import Optional

class GenreDTO(BaseModel):
    name: Optional[str] = None
