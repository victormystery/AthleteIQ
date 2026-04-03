"""
Questionnaire Response CRUD Operations
"""
from typing import Any, Dict, List, Optional, Union
from sqlalchemy.orm import Session
from datetime import datetime

from app.crud.base import CRUDBase
from app.database.models import QuestionnaireResponse
from app.models.db_schemas import QuestionnaireCreate, QuestionnaireUpdate


class CRUDQuestionnaire(CRUDBase[QuestionnaireResponse, QuestionnaireCreate, QuestionnaireUpdate]):
    """CRUD operations for QuestionnaireResponse model"""
    
    def get_by_user(self, db: Session, *, user_id: str) -> List[QuestionnaireResponse]:
        """Get all questionnaire responses for a user"""
        return db.query(QuestionnaireResponse).filter(
            QuestionnaireResponse.user_id == user_id
        ).order_by(QuestionnaireResponse.created_at.desc()).all()
    
    def get_latest_by_user(self, db: Session, *, user_id: str) -> Optional[QuestionnaireResponse]:
        """Get latest questionnaire response for a user"""
        return db.query(QuestionnaireResponse).filter(
            QuestionnaireResponse.user_id == user_id
        ).order_by(QuestionnaireResponse.created_at.desc()).first()
    
    def get_completed_by_user(self, db: Session, *, user_id: str) -> List[QuestionnaireResponse]:
        """Get completed questionnaire responses for a user"""
        return db.query(QuestionnaireResponse).filter(
            QuestionnaireResponse.user_id == user_id,
            QuestionnaireResponse.completed == True
        ).order_by(QuestionnaireResponse.created_at.desc()).all()
    
    def create_or_update(
        self, 
        db: Session, 
        *, 
        obj_in: Union[QuestionnaireCreate, Dict[str, Any]]
    ) -> QuestionnaireResponse:
        """
        Create a new questionnaire response or update existing one.
        This ensures only one questionnaire response exists per user.
        """
        # Extract user_id from the input
        if isinstance(obj_in, dict):
            user_id = obj_in.get("user_id")
            obj_data = obj_in.copy()
        else:
            user_id = obj_in.user_id
            obj_data = obj_in.model_dump()
        
        # Check if user already has a questionnaire response
        existing = self.get_latest_by_user(db, user_id=user_id)
        
        if existing:
            # Update existing response with new timestamp
            obj_data["updated_at"] = datetime.utcnow()
            return self.update(db, db_obj=existing, obj_in=obj_data)
        else:
            # Create new response
            return self.create(db, obj_in=obj_data)


questionnaire_crud = CRUDQuestionnaire(QuestionnaireResponse)
