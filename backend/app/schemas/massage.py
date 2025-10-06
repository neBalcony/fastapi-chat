from pydantic import BaseModel
from datetime import datetime


class ChatUpdate(BaseModel):
    title: str|None
    description: str|None
    
    model_config = {"from_attributes": True}

# Message schemas
class MessageBase(BaseModel):
    chat_id: int
    content: str

class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    msg_id: int
    user_id: int
    author_id: int
    created_at: datetime
    updated_at: datetime | None


class MessageEdit(MessageBase):
    msg_id: int

    model_config = {"from_attributes": True}