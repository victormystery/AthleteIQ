"""
Authentication Routes
Handles user registration, login, and profile endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from urllib.parse import quote

from app.database.session import get_db
from app.models.db_schemas import (
    UserCreate,
    User as UserSchema,
    Token,
    ProfileCreate,
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    UserInfoResponse,
)
from app.controllers.auth_controller import auth_controller
from app.config.settings import Settings, get_settings
from app.utils.auth import get_current_active_user
from app.services.google_oauth_service import get_google_oauth_service

router = APIRouter(prefix="/api/auth", tags=["authentication"])


class GoogleTokenRequest(BaseModel):
    """Google token request schema"""
    token: str


@router.post(
    "/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """
    Register a new user with profile

    Args:
        request: Combined user and profile registration data
        db: Database session

    Returns:
        User info and JWT access token
    """
    return await auth_controller.register(
        request.user_data, request.profile_data, db, settings
    )


@router.post("/login", response_model=LoginResponse)
async def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    """
    Login user and return JWT token with user information

    Args:
        payload: User login data with email and password
        db: Database session
        settings: Application settings

    Returns:
        JWT access token with user and profile information (AuthResponse)
    """
    return await auth_controller.login(payload.email, payload.password, db, settings)


@router.get("/me", response_model=UserInfoResponse)
async def get_current_user_info(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get current authenticated user information with profile

    Args:
        current_user: Authenticated user from JWT token
        db: Database session

    Returns:
        User info with profile
    """
    return await auth_controller.get_current_user_info(current_user, db)


@router.get("/check-role", response_model=dict)
async def check_user_role(
    current_user: UserSchema = Depends(get_current_active_user),
):
    """
    Check if current user is admin or student

    Args:
        current_user: Authenticated user from JWT token

    Returns:
        User role information
    """
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "is_admin": current_user.role == "admin",
        "is_student": current_user.role == "student",
    }


# Google OAuth Routes
@router.get("/google/login", response_model=dict)
async def google_login(
    settings: Settings = Depends(get_settings)
):
    """
    Initiate Google OAuth login flow
    
    Returns:
        Google OAuth authorization URL
    """
    try:
        google_service = get_google_oauth_service(settings)
        auth_data = await google_service.get_authorization_url()
        return auth_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate Google login: {str(e)}"
        )


@router.get("/google/callback")
async def google_callback(
    code: str,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings)
):
    """
    Handle Google OAuth callback
    
    Args:
        code: Authorization code from Google
        db: Database session
        settings: Application settings
        
    Returns:
        Redirect to frontend with token
    """
    try:
        # Exchange code for token and get user info
        google_service = get_google_oauth_service(settings)
        token_data = await google_service.exchange_code_for_token(code)
        user_info = token_data['user_info']
        
        # Authenticate or register user
        auth_response = await auth_controller.google_login(user_info, db, settings)
        
        # Redirect to frontend with token
        frontend_url = settings.FRONTEND_URL
        access_token = auth_response['access_token']
        redirect_url = f"{frontend_url}/auth/callback?token={access_token}"
        
        return RedirectResponse(url=redirect_url)
        
    except HTTPException as e:
        # Redirect to frontend with error message
        frontend_url = settings.FRONTEND_URL
        error_message = str(e.detail) if hasattr(e, 'detail') else 'Authentication failed'
        redirect_url = f"{frontend_url}/auth/callback?error={quote(error_message)}"
        return RedirectResponse(url=redirect_url)
    except Exception as e:
        # Redirect to frontend with generic error
        frontend_url = settings.FRONTEND_URL
        error_message = 'An unexpected error occurred during authentication'
        redirect_url = f"{frontend_url}/auth/callback?error={quote(error_message)}"
        return RedirectResponse(url=redirect_url)


@router.post("/google/verify", response_model=LoginResponse)
async def google_verify_token(
    request: GoogleTokenRequest,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings)
):
    """
    Verify Google ID token and authenticate user
    
    Args:
        request: Google token request
        db: Database session
        settings: Application settings
        
    Returns:
        JWT access token with user information
    """
    try:
        # Verify Google token
        google_service = get_google_oauth_service(settings)
        user_info = await google_service.verify_token(request.token)
        
        # Authenticate or register user
        auth_response = await auth_controller.google_login(user_info, db, settings)
        
        return auth_response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Google token verification failed: {str(e)}"
        )
