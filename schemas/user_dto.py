from pydantic import BaseModel, EmailStr
from typing import Optional

class UserDTO(BaseModel):
    id: Optional[int]=None
    username: Optional[str]=None
    email: Optional[EmailStr]=None
    password: Optional[str]=None
