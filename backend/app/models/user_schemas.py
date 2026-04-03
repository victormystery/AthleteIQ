"""
User & Authentication Schemas
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

from app.models.base_mixins import (
    DBModelMixin,
    ValidatedEmailMixin,
    ValidatedPasswordMixin,
    ValidatedNameMixin
)


class UserBase(ValidatedEmailMixin, BaseModel):
    """Base user schema"""
    email: EmailStr


class UserCreate(ValidatedPasswordMixin, ValidatedNameMixin, UserBase):
    """User creation schema"""
    password: Optional[str] = Field(None, description="Password (min 8 characters, must contain uppercase, lowercase, number, and special character). Optional for OAuth users.")
    full_name: Optional[str] = Field(None, description="User's full name (string only)")
    role: Optional[str] = "student"


class UserUpdate(ValidatedPasswordMixin, ValidatedEmailMixin, BaseModel):
    """User update schema"""
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase, DBModelMixin):
    """User response schema"""
    id: str
    full_name: Optional[str] = None
    role: str
    is_active: bool
    oauth_provider: Optional[str] = None
    email_verified: bool = False
    avatar_url: Optional[str] = None
    created_at: datetime


class Token(BaseModel):
    """JWT Token schema"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema"""
    email: Optional[str] = None
    user_id: Optional[str] = None


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str
