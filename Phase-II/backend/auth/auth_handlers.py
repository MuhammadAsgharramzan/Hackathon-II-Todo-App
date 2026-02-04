from passlib.context import CryptContext
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from sqlmodel import Session, select
from models.user_model import User, UserCreate
from fastapi import HTTPException, status
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bcrypt context with error handling for compatibility
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
except Exception:
    # Fallback to auto-detection if there are issues with bcrypt version
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt, truncating if necessary"""
    # Bcrypt has a 72-byte password limit
    truncated_password = password[:72] if len(password) > 72 else password
    return pwd_context.hash(truncated_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Retrieve a user by email"""
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def create_user(session: Session, user_create: UserCreate) -> User:
    """Create a new user with hashed password"""
    # Check if user already exists
    existing_user = get_user_by_email(session, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )

    hashed_password = hash_password(user_create.password)
    db_user = User(
        email=user_create.email,
        hashed_password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    logger.info(f"User created successfully: {db_user.email}")

    return db_user


def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password"""
    user = get_user_by_email(session, email)

    if not user or not verify_password(password, user.hashed_password):
        logger.warning(f"Failed authentication attempt for email: {email}")
        return None

    logger.info(f"User authenticated successfully: {user.email}")

    return user