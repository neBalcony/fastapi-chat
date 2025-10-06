from pydantic import BaseModel
from typing import Optional, List


# User schemas
class UserBase(BaseModel):
    username: str

class UserPublic(BaseModel):
    id:int
    
class UsersPublic(BaseModel):
    users: List[UserPublic]

class UserRegister(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    model_config = {"from_attributes": True}


