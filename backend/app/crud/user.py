"""
User CRUD Operations
"""
from typing import Optional, Union, Dict, Any
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.crud.base import CRUDBase
from app.database.models import User
from app.models.db_schemas import UserCreate, UserUpdate

# Use pbkdf2_sha256 to avoid C-extension dependencies (bcrypt issues on some environments).
# If you prefer bcrypt in production, ensure the `bcrypt` package is correctly installed.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """CRUD operations for User model"""
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    def create(self, db: Session, *, obj_in: Union[UserCreate, Dict[str, Any]], 
               oauth_provider: Optional[str] = None,
               oauth_user_id: Optional[str] = None,
               email_verified: bool = False,
               avatar_url: Optional[str] = None) -> User:
        """Create new user with hashed password or OAuth info"""
        # Handle both Pydantic model and dict
        if isinstance(obj_in, dict):
            email = obj_in.get("email")
            full_name = obj_in.get("full_name")
            password = obj_in.get("password")
            role = obj_in.get("role", "student")
        else:
            email = obj_in.email
            full_name = obj_in.full_name if hasattr(obj_in, 'full_name') else None
            password = obj_in.password
            role = obj_in.role if hasattr(obj_in, 'role') and obj_in.role else "student"
        
        # Hash password if provided, otherwise null for OAuth users
        hashed_password = None
        if password and password.strip():
            hashed_password = self.get_password_hash(password)
        elif not oauth_provider:
            raise ValueError("Password is required for non-OAuth users")
        
        db_obj = User(
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
            role=role,
            oauth_provider=oauth_provider,
            oauth_user_id=oauth_user_id,
            email_verified=email_verified,
            avatar_url=avatar_url
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """Authenticate user"""
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        
        # OAuth users cannot authenticate with password
        if user.oauth_provider and not user.hashed_password:
            return None
        
        # Type assertion: SQLAlchemy models return actual values at runtime
        hashed_password: str = user.hashed_password  # type: ignore
        if not hashed_password or not self.verify_password(password, hashed_password):
            return None
        return user
    
    def is_active(self, user: User) -> bool:
        """Check if user is active"""
        # Type assertion: SQLAlchemy models return actual values at runtime
        is_active: bool = user.is_active  # type: ignore
        return is_active
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash password"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        return pwd_context.verify(plain_password, hashed_password)


user_crud = CRUDUser(User)
