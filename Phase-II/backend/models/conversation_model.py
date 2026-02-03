from sqlmodel import SQLModel, Field, Column, DateTime
from typing import Optional
import datetime
from enum import Enum


class RoleEnum(str, Enum):
    user = "user"
    assistant = "assistant"


class ConversationBase(SQLModel):
    user_id: str = Field(index=True)  # From JWT token


class Conversation(ConversationBase, table=True):
    id: int = Field(primary_key=True)
    created_at: datetime.datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    )


class MessageBase(SQLModel):
    conversation_id: int = Field(foreign_key="conversation.id")
    user_id: str = Field(index=True)  # From JWT token
    role: RoleEnum
    content: str = Field(max_length=10000)


class Message(MessageBase, table=True):
    id: int = Field(primary_key=True)
    created_at: datetime.datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
    )


class ConversationCreate(ConversationBase):
    pass


class ConversationResponse(ConversationBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: int
    created_at: datetime.datetime