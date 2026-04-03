"""
Authentication Controller
Handles user registration, login, and authentication
"""
import logging
from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict

from app.config.settings import Settings
from app.crud.user import user_crud
from app.crud.profile import profile_crud
from app.models.db_schemas import UserCreate, User, Token, ProfileCreate, RegisterResponse
from app.utils.auth import create_access_token

logger = logging.getLogger(__name__)


class AuthController:
    """Controller for authentication endpoints"""
    
    @staticmethod
    async def register(
        user_data: UserCreate,
        profile_data: ProfileCreate,
        db: Session,
        settings: Settings
    ) -> dict:
        """
        Register a new user with profile
        
        Args:
            user_data: User registration data
            profile_data: User profile data
            db: Database session
            
        Returns:
            User and access token
        """
        try:
            # Validate that password is provided for non-OAuth registration
            if not user_data.password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Password is required for registration"
                )
            
            # Check if user already exists
            existing_user = user_crud.get_by_email(db, email=user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            
            # Create user
            user = user_crud.create(db, obj_in=user_data)
            
            # Sync full_name from user to profile if profile doesn't have it
            profile_dict = profile_data.model_dump()
            profile_full_name = profile_dict.get("full_name")
            if user.full_name is not None and profile_full_name is None:
                profile_dict["full_name"] = user.full_name
            
            # Create profile for user with provided data
            profile = profile_crud.create_for_user(db, obj_in=profile_dict, user_id=str(user.id))
            
            # Create access token
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                subject=str(user.email),
                settings=settings,
                expires_delta=access_token_expires,
                user_id=str(user.id),
                role=str(user.role)
            )
            
            logger.info(f"✅ User registered: {user.email}")
            
            return {
                "user": user,
                "profile": profile,
                "access_token": access_token,
                "token_type": "bearer"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error during registration: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Registration failed: {str(e)}"
            )
    
    @staticmethod
    async def login(email: str, password: str, db: Session, settings: Settings) -> dict:
        """
        Authenticate user and return access token with user info
        
        Args:
            email: User email
            password: User password
            db: Database session
            settings: Application settings
            
        Returns:
            Access token with user and profile information
        """
        try:
            # Authenticate user
            user = user_crud.authenticate(db, email=email, password=password)
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            if not user_crud.is_active(user):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Inactive user"
                )
            
            # Get user profile
            profile = profile_crud.get_by_user_id(db, user_id=str(user.id))
            
            # Sync full_name from user to profile if needed
            if profile is not None and user.full_name is not None:
                if profile.full_name is None or profile.full_name.strip() == "":
                    profile_crud.update(db, db_obj=profile, obj_in={"full_name": user.full_name})
                    profile = profile_crud.get_by_user_id(db, user_id=str(user.id))
            
            # Create access token
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                subject=str(user.email),
                settings=settings,
                expires_delta=access_token_expires,
                user_id=str(user.id),
                role=str(user.role)
            )
            
            logger.info(f"✅ User logged in: {user.email}")
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": user,
                "profile": profile
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Login failed: {str(e)}"
            )
    
    @staticmethod
    async def get_current_user_info(user: User, db: Session) -> dict:
        """
        Get current user information including profile
        
        Args:
            user: Current authenticated user
            db: Database session
            
        Returns:
            User info with profile
        """
        try:
            # Get user profile
            profile = profile_crud.get_by_user_id(db, user_id=user.id)
            
            # Sync full_name from user to profile if needed
            if profile is not None and user.full_name is not None and (profile.full_name is None or (isinstance(profile.full_name, str) and profile.full_name.strip() == "")):
                profile_crud.update(db, db_obj=profile, obj_in={"full_name": user.full_name})
                profile = profile_crud.get_by_user_id(db, user_id=user.id)
            
            return {
                "user": user,
                "profile": profile
            }
            
        except Exception as e:
            logger.error(f"Error getting user info: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get user info: {str(e)}"
            )
    
    @staticmethod
    async def google_login(google_user_info: Dict, db: Session, settings: Settings) -> dict:
        """
        Authenticate or register user via Google OAuth
        
        Args:
            google_user_info: User info from Google
            db: Database session
            settings: Application settings
            
        Returns:
            Access token with user and profile information
        """
        try:
            email = google_user_info.get('email')
            google_id = google_user_info.get('google_id')
            
            if not email or not google_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid Google user information"
                )
            
            # Check if user exists by email or google_id
            user = user_crud.get_by_email(db, email=email)
            
            if user:
                # Update existing user with Google OAuth info if not already set
                if not user.oauth_provider:
                    update_data = {
                        'oauth_provider': 'google',
                        'oauth_user_id': google_id,
                        'email_verified': google_user_info.get('email_verified', False),
                        'avatar_url': google_user_info.get('picture')
                    }
                    user = user_crud.update(db, db_obj=user, obj_in=update_data)
                
                logger.info(f"✅ Existing user logged in via Google: {email}")
            else:
                # Create new user from Google OAuth
                user_data = UserCreate(
                    email=email,
                    password=None,  # No password for OAuth users
                    full_name=google_user_info.get('name'),
                    role='student'
                )
                
                # Create user with OAuth info
                user = user_crud.create(
                    db,
                    obj_in=user_data,
                    oauth_provider='google',
                    oauth_user_id=google_id,
                    email_verified=google_user_info.get('email_verified', False),
                    avatar_url=google_user_info.get('picture')
                )
                
                # Create profile for new user
                profile_data = {
                    'full_name': google_user_info.get('name'),
                    'avatar_url': google_user_info.get('picture')
                }
                profile_crud.create_for_user(db, obj_in=profile_data, user_id=str(user.id))
                
                logger.info(f"✅ New user registered via Google: {email}")
            
            # Get user profile
            profile = profile_crud.get_by_user_id(db, user_id=str(user.id))
            
            # Create access token
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                subject=str(user.email),
                settings=settings,
                expires_delta=access_token_expires,
                user_id=str(user.id),
                role=str(user.role)
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": user,
                "profile": profile
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error during Google login: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Google login failed: {str(e)}"
            )


auth_controller = AuthController()
