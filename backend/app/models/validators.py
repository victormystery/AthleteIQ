"""
Pydantic Validators for Database Schemas
Reusable validation functions for user and profile data
"""
import re
from typing import Optional


# ============================================
# Email Validators
# ============================================

def validate_email_format(v: str) -> str:
    """
    Validate email format
    
    Args:
        v: Email string to validate
        
    Returns:
        Normalized email (lowercase, trimmed)
        
    Raises:
        ValueError: If email is invalid
    """
    if not v or len(v) == 0:
        raise ValueError('Email cannot be empty')
    
    if len(v) > 255:
        raise ValueError('Email must not exceed 255 characters')
    
    # EmailStr from pydantic already validates, but adding additional checks
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
        raise ValueError('Invalid email format')
    
    return v.lower().strip()


# ============================================
# Password Validators
# ============================================

def validate_password_strength(v: Optional[str]) -> Optional[str]:
    """
    Validate that password is strong
    
    Requirements:
    - At least 8 characters
    - At least one uppercase letter (A-Z)
    - At least one lowercase letter (a-z)
    - At least one digit (0-9)
    - At least one special character (!@#$%^&*(),.?":{}|<>)
    
    Args:
        v: Password string to validate (optional for OAuth users)
        
    Returns:
        The password if valid
        
    Raises:
        ValueError: If password doesn't meet requirements
    """
    # Allow None or empty string for OAuth users
    if v is None or v == "":
        return v
    
    if len(v) < 8:
        raise ValueError('Password must be at least 8 characters long')
    
    if not re.search(r'[A-Z]', v):
        raise ValueError('Password must contain at least one uppercase letter')
    
    if not re.search(r'[a-z]', v):
        raise ValueError('Password must contain at least one lowercase letter')
    
    if not re.search(r'[0-9]', v):
        raise ValueError('Password must contain at least one digit')
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
        raise ValueError('Password must contain at least one special character (!@#$%^&*(),.?":{}|<>)')
    
    return v


# ============================================
# Full Name Validators
# ============================================

def validate_full_name(v: Optional[str]) -> Optional[str]:
    """
    Validate that full_name is a string and contains only allowed characters
    
    Requirements:
    - Must be a string (if provided)
    - 2-100 characters
    - Only letters, spaces, hyphens, and apostrophes allowed
    
    Args:
        v: Full name string to validate (optional)
        
    Returns:
        Normalized full name (trimmed)
        
    Raises:
        ValueError: If full name is invalid
    """
    if v is None:
        return v
    
    if not isinstance(v, str):
        raise ValueError('Full name must be a string')
    
    if len(v.strip()) == 0:
        raise ValueError('Full name cannot be empty')
    
    if len(v) > 100:
        raise ValueError('Full name must not exceed 100 characters')
    
    # Allow letters, spaces, hyphens, apostrophes
    if not re.match(r"^[a-zA-Z\s\-']+$", v):
        raise ValueError('Full name can only contain letters, spaces, hyphens, and apostrophes')
    
    return v.strip()
