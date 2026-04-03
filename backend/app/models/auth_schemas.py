"""
Authentication Response Schemas
"""
from pydantic import BaseModel

from app.models.user_schemas import User, UserCreate
from app.models.profile_schemas import Profile, ProfileCreate


class RegisterRequest(BaseModel):
    """Combined registration request schema"""
    user_data: UserCreate
    profile_data: ProfileCreate


class AuthResponse(BaseModel):
    """Authentication response with token and user info"""
    access_token: str
    token_type: str = "bearer"
    user: User
    profile: Profile


class UserInfoResponse(BaseModel):
    """User information response (without token)"""
    user: User
    profile: Profile


# Aliases for clarity
RegisterResponse = AuthResponse
LoginResponse = AuthResponse
