"""
Base Mixins for Schema Models
Reusable mixins for common functionality
"""
from pydantic import ConfigDict, field_validator

from app.models.validators import (
    validate_email_format,
    validate_password_strength,
    validate_full_name
)


class DBModelMixin:
    """Mixin for database response models"""
    model_config = ConfigDict(from_attributes=True)


class ValidatedEmailMixin:
    """Mixin for email validation"""
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v is None:
            return v
        return validate_email_format(v)


class ValidatedPasswordMixin:
    """Mixin for password validation"""
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        return validate_password_strength(v)


class ValidatedNameMixin:
    """Mixin for full name validation"""
    @field_validator('full_name')
    @classmethod
    def validate_name(cls, v):
        return validate_full_name(v)
