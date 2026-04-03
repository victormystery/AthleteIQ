"""
Profile Controller
Handles user profile operations
"""
import logging
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.profile import profile_crud
from app.models.db_schemas import ProfileUpdate, User, Profile as ProfileSchema

logger = logging.getLogger(__name__)


class ProfileController:
    """Controller for profile endpoints"""
    
    @staticmethod
    async def get_profile(user: User, db: Session) -> dict:
        """
        Get user profile
        
        Args:
            user: Current authenticated user
            db: Database session
            
        Returns:
            User profile
        """
        try:
            profile = profile_crud.get_by_user_id(db, user_id=user.id)
            
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            # Convert SQLAlchemy model to Pydantic schema
            profile_schema = ProfileSchema.model_validate(profile)
            return {"profile": profile_schema}
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting profile: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get profile: {str(e)}"
            )
    
    @staticmethod
    async def update_profile(
        user: User,
        profile_data: ProfileUpdate,
        db: Session
    ) -> dict:
        """
        Update user profile
        
        Args:
            user: Current authenticated user
            profile_data: Profile update data
            db: Database session
            
        Returns:
            Updated profile
        """
        try:
            profile = profile_crud.get_by_user_id(db, user_id=user.id)
            
            if not profile:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profile not found"
                )
            
            # Update profile
            updated_profile = profile_crud.update(
                db,
                db_obj=profile,
                obj_in=profile_data
            )
            
            logger.info(f"✅ Profile updated for user: {user.email}")
            
            # Convert SQLAlchemy model to Pydantic schema
            profile_schema = ProfileSchema.model_validate(updated_profile)
            return {"profile": profile_schema}
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating profile: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update profile: {str(e)}"
            )


profile_controller = ProfileController()
