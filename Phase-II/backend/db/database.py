from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy import event
from sqlalchemy.engine import Engine
import os
from typing import Generator
from models.user_model import User  # Import user model to register it
from models.task_model import Task  # Import all models to register them
from models.conversation_model import Conversation, Message  # Import conversation models to register them


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session"""
    with Session(engine) as session:
        yield session