"""
Authentication Utilities
JWT token creation and verification with password hashing
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.config.settings import Settings, get_settings
from app.database.session import get_db
from app.crud.user import user_crud
from app.database.models import User

bearer_scheme = HTTPBearer(auto_error=False)

# Use pbkdf2_sha256 to avoid C-extension dependencies (bcrypt issues on some environments).
# If you prefer bcrypt in production, ensure the `bcrypt` package is correctly installed.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Hash a password for storing"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: str,
    settings: Settings,
    expires_delta: Optional[timedelta] = None,
    **extra_claims
) -> str:
    """
    Create JWT access token
    
    Args:
        subject: Subject (usually email or user ID)
        expires_delta: Token expiration time
        **extra_claims: Additional claims to add to the token (e.g., role)
        
    Returns:
        Encoded JWT token
    """
    now = datetime.now(timezone.utc)
    if expires_delta:
        exp = now + expires_delta
    else:
        exp = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": exp, "iat": now}
    # Merge any extra claims (like role) into the payload
    if extra_claims:
        payload.update(extra_claims)
    token = jwt.encode(payload, settings.get_jwt_secret(), algorithm=settings.JWT_ALGORITHM)
    return token


def decode_access_token(token: str, settings: Settings) -> dict:
    """Decode a JWT token"""
    return jwt.decode(token, settings.get_jwt_secret(), algorithms=[settings.JWT_ALGORITHM])


def verify_token(token: str, settings: Settings) -> str:
    """
    Verify JWT token and return username
    
    Args:
        token: JWT token to verify
        
    Returns:
        Username/email from token
        
    Raises:
        HTTPException: If token is invalid
    """
    try:
        payload = decode_access_token(token, settings)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username not found in token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings)
) -> User:
    """
    Get current authenticated user
    
    Args:
        credentials: HTTP Bearer credentials from Authorization header
        db: Database session
        
    Returns:
        Current user object
    """
    token = credentials.credentials
    email = verify_token(token, settings)
    user = user_crud.get_by_email(db, email=email)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current active user object
    """
    if not user_crud.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return current_user


# Optional user dependency (allows endpoints to work with or without auth)
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings)
) -> Optional[User]:
    """
    Get current user if authenticated, None otherwise
    Allows endpoints to work with or without authentication
    """
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials, db, settings)
    except HTTPException:
        return None
