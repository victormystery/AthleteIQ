"""
Google OAuth Service
Handles Google OAuth2 authentication flow
"""
import logging
from typing import Optional, Dict
from fastapi import HTTPException, status
from google.oauth2 import id_token
from google.auth.transport import requests
from authlib.integrations.starlette_client import OAuth

from app.config.settings import Settings

logger = logging.getLogger(__name__)


class GoogleOAuthService:
    """Service for Google OAuth authentication"""
    
    def __init__(self, settings: Settings):
        """Initialize Google OAuth service"""
        self.settings = settings
        self.oauth = OAuth()
        
        # Register Google OAuth client
        self.oauth.register(
            name='google',
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={
                'scope': 'openid email profile',
                'redirect_uri': settings.GOOGLE_REDIRECT_URI
            }
        )
    
    async def get_authorization_url(self, redirect_uri: Optional[str] = None) -> Dict[str, str]:
        """
        Generate Google OAuth authorization URL
        
        Args:
            redirect_uri: Optional custom redirect URI
            
        Returns:
            Dictionary with authorization URL and state
        """
        try:
            if redirect_uri:
                self.oauth.google.client_kwargs['redirect_uri'] = redirect_uri
            
            # Generate authorization URL with state parameter
            authorization_url = f"https://accounts.google.com/o/oauth2/v2/auth?" \
                              f"client_id={self.settings.GOOGLE_CLIENT_ID}&" \
                              f"redirect_uri={self.settings.GOOGLE_REDIRECT_URI}&" \
                              f"response_type=code&" \
                              f"scope=openid email profile&" \
                              f"access_type=offline&" \
                              f"prompt=consent"
            
            return {
                "authorization_url": authorization_url,
                "redirect_uri": self.settings.GOOGLE_REDIRECT_URI
            }
            
        except Exception as e:
            logger.error(f"Error generating authorization URL: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate authorization URL: {str(e)}"
            )
    
    async def verify_token(self, token: str) -> Dict:
        """
        Verify Google ID token and extract user information
        
        Args:
            token: Google ID token
            
        Returns:
            Dictionary with user information
        """
        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                self.settings.GOOGLE_CLIENT_ID
            )
            
            # Verify issuer
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            
            # Extract user information
            user_info = {
                'email': idinfo.get('email'),
                'email_verified': idinfo.get('email_verified', False),
                'name': idinfo.get('name'),
                'picture': idinfo.get('picture'),
                'google_id': idinfo.get('sub'),
                'given_name': idinfo.get('given_name'),
                'family_name': idinfo.get('family_name'),
            }
            
            logger.info(f"✅ Google token verified for: {user_info['email']}")
            return user_info
            
        except ValueError as e:
            logger.error(f"Invalid Google token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid Google token: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Error verifying Google token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to verify Google token: {str(e)}"
            )
    
    async def exchange_code_for_token(self, code: str) -> Dict:
        """
        Exchange authorization code for access token
        
        Args:
            code: Authorization code from Google
            
        Returns:
            Dictionary with token information
        """
        try:
            import httpx
            
            # Exchange code for token
            token_url = "https://oauth2.googleapis.com/token"
            data = {
                'code': code,
                'client_id': self.settings.GOOGLE_CLIENT_ID,
                'client_secret': self.settings.GOOGLE_CLIENT_SECRET,
                'redirect_uri': self.settings.GOOGLE_REDIRECT_URI,
                'grant_type': 'authorization_code'
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(token_url, data=data)
                
                if response.status_code != 200:
                    logger.error(f"Token exchange failed: {response.text}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Failed to exchange authorization code"
                    )
                
                token_data = response.json()
                
                # Verify and decode ID token
                user_info = await self.verify_token(token_data['id_token'])
                
                return {
                    'access_token': token_data.get('access_token'),
                    'id_token': token_data.get('id_token'),
                    'user_info': user_info
                }
                
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error exchanging code for token: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to exchange authorization code: {str(e)}"
            )


# Global instance
google_oauth_service: Optional[GoogleOAuthService] = None


def get_google_oauth_service(settings: Settings) -> GoogleOAuthService:
    """Get or create Google OAuth service instance"""
    global google_oauth_service
    if google_oauth_service is None:
        google_oauth_service = GoogleOAuthService(settings)
    return google_oauth_service
