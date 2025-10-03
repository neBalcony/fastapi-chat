# SQLAlchemy models for a chat app: User, Chat, Message
import enum
from sqlalchemy import Column, Enum, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="user")
    chats = relationship("Chat", secondary="user_chats", back_populates="users")

class ChatType(enum.Enum):
	dm = "dm"
	grup = "grup"

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    type = Column(
        Enum(ChatType, name="chat_type_enum", native_enum=False), 
        nullable=False,
    )
    messages = relationship("Message", back_populates="chat")
    users = relationship("User", secondary="user_chats", back_populates="chats")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)

    user = relationship("User", back_populates="messages")
    chat = relationship("Chat", back_populates="messages")

class UserChat(Base):
    __tablename__ = "user_chats"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), primary_key=True)
