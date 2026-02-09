from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
import hashlib
from ..models.user import User
from .config import settings
import uuid

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security schemes
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.
    Handles both bcrypt and SHA-256 hashed passwords for environment compatibility.
    """
    # Check if this is a SHA-256 hashed password (for environment compatibility)
    if hashed_password.startswith('sha256:'):
        # Extract the stored hash
        stored_hash = hashed_password[7:]  # Remove 'sha256:' prefix

        # Create SHA-256 hash of the input password
        input_hash = hashlib.sha256(plain_password.encode()).hexdigest()

        # Compare the hashes
        return input_hash == stored_hash

    # Otherwise, use bcrypt (if it works in the environment)
    try:
        # Bcrypt has a 72-byte password length limit
        # We need to truncate the password to 72 bytes before verifying
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            # Truncate to 72 bytes and decode back to string
            plain_password = password_bytes[:72].decode('utf-8', errors='ignore')

        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        # If bcrypt fails, try SHA-256 fallback
        if hashed_password.startswith('sha256:'):
            stored_hash = hashed_password[7:]
            input_hash = hashlib.sha256(plain_password.encode()).hexdigest()
            return input_hash == stored_hash
        return False

def get_password_hash(password: str) -> str:
    """
    Generate a hash for a plaintext password.
    Uses SHA-256 fallback for environment compatibility with bcrypt issues.
    """
    try:
        # Bcrypt has a 72-byte password length limit
        # We need to truncate the password to 72 bytes before hashing
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 71:  # Using 71 to stay safely under the limit
            # Truncate to 71 bytes and decode back to string
            password = password_bytes[:71].decode('utf-8', errors='ignore')

        return pwd_context.hash(password)
    except Exception:
        # If bcrypt fails, use SHA-256 as fallback for environment compatibility
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return f"sha256:{password_hash}"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token with the provided data and expiration.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT refresh token with the provided data and expiration.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)

    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """
    Verify a JWT token and return the payload if valid, None otherwise.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None

async def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Get the current user from the JWT token in the Authorization header.
    This function verifies the token and returns the user data from the token payload.
    """
    token = credentials.credentials

    # Verify the token
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if it's an access token
    token_type = payload.get("type")
    if token_type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user data from the token
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convert user_id to UUID if it's a string representation
    try:
        user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Return user data from the token (no database lookup needed)
    return {
        "id": user_uuid,
        "email": payload.get("email"),
    }

def get_user_id_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> uuid.UUID:
    """
    Extract and return the user_id from the JWT token in the Authorization header.
    This is used to enforce that user_id comes from the token, not from request parameters.
    """
    token = credentials.credentials

    # Verify the token
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if it's an access token
    token_type = payload.get("type")
    if token_type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user_id from the token
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convert user_id to UUID if it's a string representation
    try:
        user_uuid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_uuid