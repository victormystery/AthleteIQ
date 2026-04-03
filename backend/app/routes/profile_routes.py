"""
Profile Management Routes
Handles user profile operations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.db_schemas import (
    Profile as ProfileSchema,
    ProfileUpdate,
    ProfileResponse,
    User as UserSchema
)
from app.controllers.profile_controller import profile_controller
from app.utils.auth import get_current_active_user

router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.get("/me", response_model=ProfileResponse)
async def get_current_user_profile(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's profile
    
    Args:
        current_user: Authenticated user
        db: Database session
        
    Returns:
        User profile
    """
    return await profile_controller.get_profile(current_user, db)



@router.put("/me", response_model=ProfileResponse)
async def update_current_user_profile(
    profile_data: ProfileUpdate,
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile
    
    Args:
        profile_data: Profile fields to update
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Updated profile
    """
    return await profile_controller.update_profile(current_user, profile_data, db)


