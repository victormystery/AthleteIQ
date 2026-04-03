"""
Profile Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.models.base_mixins import DBModelMixin, ValidatedNameMixin


class ProfileFieldsMixin(BaseModel):
    """Common profile fields"""
    full_name: Optional[str] = Field(None, max_length=100, description="User's full name")
    avatar_url: Optional[str] = Field(None, max_length=500, description="URL to user's avatar image")
    university: Optional[str] = Field(None, max_length=200, description="University or institution name")
    programme_of_study: Optional[str] = Field(None, max_length=200, description="Academic program or course of study")
    year_of_study: Optional[int] = Field(None, ge=1, le=7, description="Current year of study (1-7)")
    primary_sport: Optional[str] = Field(None, max_length=100, description="Primary sport of interest")
    phone_number: Optional[str] = Field(None, max_length=20, description="Contact phone number")


class ProfileBase(ProfileFieldsMixin):
    """Base profile schema"""
    pass


class ProfileCreate(ValidatedNameMixin, ProfileFieldsMixin):
    """Profile creation schema"""
    pass


class ProfileUpdate(ValidatedNameMixin, ProfileFieldsMixin):
    """Profile update schema"""
    pass


class Profile(ProfileFieldsMixin, DBModelMixin):
    """Profile response schema"""
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime]


class ProfileResponse(BaseModel):
    """Profile response wrapper"""
    profile: Profile
