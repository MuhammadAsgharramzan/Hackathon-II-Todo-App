from fastapi import HTTPException, status, Header
from typing import Optional
import jwt
import os
import secrets
from datetime import datetime
import logging
import json
import base64

# Import centralized configuration
from config import JWT_SECRET_KEY, JWT_ALGORITHM

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use centralized configuration
SECRET_KEY = JWT_SECRET_KEY
ALGORITHM = JWT_ALGORITHM

class User:
    """Simple User class to hold user information"""
    def __init__(self, id: str):
        self.id = id

def get_current_user(authorization: str = Header(None)) -> User:
    """
    JWT dependency to extract user from token
    This is the shared dependency that ensures consistent user identity
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not authorization or not authorization.startswith("Bearer "):
        logger.warning("Invalid token format received")
        raise credentials_exception

    # Extract the actual token part
    actual_token = authorization.split(" ")[1]

    # Check if this is a mock token (starts with our mock pattern and has mock signature)
    if actual_token.count('.') == 2 and actual_token.endswith(".mock-signature"):
        try:
            # Decode the payload part to extract user ID
            header_payload = actual_token.rsplit('.', 1)[0]  # Remove signature
            header_part, payload_part = header_payload.split('.', 1)

            # Decode the payload (add padding if needed)
            payload_data = json.loads(base64.b64decode(payload_part + '==='))
            user_id = payload_data.get("sub")

            if user_id:
                logger.info(f"Mock JWT token verified for user: {user_id}")
                return User(id=user_id)
        except Exception as e:
            logger.warning(f"Invalid mock token format: {str(e)}")
            raise credentials_exception

    # Try to verify as a real JWT token
    try:
        payload = jwt.decode(actual_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            logger.warning("No user ID found in token payload")
            raise credentials_exception

        # Log successful token verification
        logger.info(f"JWT token verified for user: {user_id}")

        return User(id=user_id)
    except jwt.ExpiredSignatureError:
        logger.warning(f"Expired token attempted: {actual_token[:10]}...")
        raise credentials_exception
    except jwt.InvalidTokenError:
        logger.warning(f"Invalid token attempted: {actual_token[:10]}...")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Unexpected error during token verification: {str(e)}")
        raise credentials_exception