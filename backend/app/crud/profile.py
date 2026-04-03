"""
Profile CRUD Operations
"""
from typing import Optional, Dict, Any, Union
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.database.models import Profile
from app.models.db_schemas import ProfileCreate, ProfileUpdate


class CRUDProfile(CRUDBase[Profile, ProfileCreate, ProfileUpdate]):
    """CRUD operations for Profile model"""
    
    def get_by_user_id(self, db: Session, *, user_id: str) -> Optional[Profile]:
        """Get profile by user ID"""
        return db.query(Profile).filter(Profile.user_id == user_id).first()
    
    def create_for_user(self, db: Session, *, obj_in: Union[ProfileCreate, Dict[str, Any]], user_id: str) -> Profile:
        """Create profile for user"""
        if isinstance(obj_in, dict):
            obj_in_data = obj_in
        else:
            obj_in_data = obj_in.model_dump()
        db_obj = Profile(**obj_in_data, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


profile_crud = CRUDProfile(Profile)
