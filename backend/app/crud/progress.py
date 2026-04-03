"""
Progress CRUD Operations
"""
from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.database.models import UserProgress
from app.models.db_schemas import ProgressCreate, ProgressUpdate


class CRUDProgress(CRUDBase[UserProgress, ProgressCreate, ProgressUpdate]):
    """CRUD operations for UserProgress model"""
    
    def get_by_user(self, db: Session, *, user_id: str) -> List[UserProgress]:
        """Get all progress for a user"""
        return db.query(UserProgress).filter(
            UserProgress.user_id == user_id
        ).order_by(UserProgress.created_at.desc()).all()
    
    def get_by_user_and_pathway(
        self, 
        db: Session, 
        *, 
        user_id: str, 
        pathway_id: str
    ) -> List[UserProgress]:
        """Get progress for a user on a specific pathway"""
        return db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.pathway_id == pathway_id
        ).order_by(UserProgress.created_at.desc()).all()
    
    def get_completed_count(self, db: Session, *, user_id: str) -> int:
        """Get count of completed progress items"""
        return db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.status == "completed"
        ).count()


progress_crud = CRUDProgress(UserProgress)
