from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
	username: str

class UserCreate(UserBase):
	password: str

class UserRead(UserBase):
	id: int
	created_at: datetime

	class Config:
		orm_mode = True
		
# Chat schemas
class ChatBase(BaseModel):
	title: Optional[str] = None

class ChatCreate(ChatBase):
	pass

class ChatRead(ChatBase):
	id: int
	created_at: datetime
	users: List[UserRead] = []

	class Config:
		orm_mode = True

# Message schemas
class MessageBase(BaseModel):
	content: str

class MessageCreate(MessageBase):
	chat_id: int

class MessageRead(MessageBase):
	id: int
	timestamp: datetime
	user_id: int
	chat_id: int
	user: Optional[UserRead]

	class Config:
		orm_mode = True

# UserChat schema (for completeness, usually not exposed directly)
class UserChatRead(BaseModel):
	user_id: int
	chat_id: int
	joined_at: datetime

	class Config:
		orm_mode = True
