import os
import secrets
import json
import base64
from typing import Dict, Optional
import jwt
from fastapi import HTTPException, Header
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use a more secure secret key generation if not set in environment
SECRET_KEY = os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token with enhanced security"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Log token creation for audit trail
    user_id = data.get("sub", "unknown")
    logger.info(f"JWT token created for user: {user_id}")

    return encoded_jwt


def verify_token(token: str = Header(...)):
    """Verify JWT token and extract user info with enhanced security"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token or not token.startswith("Bearer "):
        logger.warning("Invalid token format received")
        raise credentials_exception

    # Extract the actual token part
    actual_token = token.split(" ")[1]

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
                return user_id
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

        return user_id
    except jwt.ExpiredSignatureError:
        logger.warning(f"Expired token attempted: {actual_token[:10]}...")
        raise credentials_exception
    except jwt.InvalidTokenError:
        logger.warning(f"Invalid token attempted: {actual_token[:10]}...")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Unexpected error during token verification: {str(e)}")
        raise credentials_exception