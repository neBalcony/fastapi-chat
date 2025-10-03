from pydantic import BaseModel,EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

# User schemas
class UserBase(BaseModel):
	username: str

class UserCreate(UserBase):
	password: str
	email: EmailStr
	display_name: str|None = None
	avatar_url: str|None = None

class UserRead(UserBase):
	id: int
	email: EmailStr
	display_name: str|None = None
	avatar_url: str|None = None
	status: str|None = None
	created_at: datetime|None = None

	class Config:
		orm_mode = True

# Chat schemas
class ChatType(str, Enum):
	dm = "dm"
	grup = "grup"

class ChatBase(BaseModel):
	title: str
	description: str
	type: ChatType
	users: List[UserRead] = []

class ChatCreate(ChatBase):
	pass

class ChatRead(ChatBase):
	id: int
	created_at: datetime
	created_by: int #user id

	class Config:
		orm_mode = True

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

	class Config:
		orm_mode = True
