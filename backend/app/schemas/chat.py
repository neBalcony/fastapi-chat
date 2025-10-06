from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum
from .user import UserRead 

# Chat schemas
class ChatType(str, Enum):
    dm = "dm"
    grup = "grup"


class ChatCreate(BaseModel):
    title: str
    description: str
    type: ChatType
    users: List[int] = []


class ChatRead(BaseModel):
    id: int
    title: str
    description: str
    type: ChatType
    users: List[UserRead] = []

    created_at: datetime
    model_config = {"from_attributes": True}

class ChatUpdate(BaseModel):
    title: str|None
    description: str|None
    
    model_config = {"from_attributes": True}


class ChatRemoveUsers(BaseModel):
    removed_users: List[int]
    
class ChatAddUsers(BaseModel):
    added_users: List[int]

