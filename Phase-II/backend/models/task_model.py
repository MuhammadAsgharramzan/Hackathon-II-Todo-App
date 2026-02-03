from sqlmodel import SQLModel, Field, Column, DateTime
from typing import Optional
import datetime


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    id: int = Field(primary_key=True)
    user_id: str = Field(index=True)  # From JWT token
    created_at: datetime.datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now)
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    )


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)


class TaskResponse(TaskBase):
    id: int
    user_id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime