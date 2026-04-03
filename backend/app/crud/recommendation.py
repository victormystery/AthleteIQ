"""
Recommendation CRUD Operations
"""
from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.database.models import PathwayRecommendation
from app.models.db_schemas import RecommendationCreate, RecommendationUpdate


class CRUDRecommendation(CRUDBase[PathwayRecommendation, RecommendationCreate, RecommendationUpdate]):
    """CRUD operations for PathwayRecommendation model"""
    
    def get_by_user(self, db: Session, *, user_id: str) -> List[PathwayRecommendation]:
        """Get all recommendations for a user"""
        return db.query(PathwayRecommendation).filter(
            PathwayRecommendation.user_id == user_id
        ).order_by(PathwayRecommendation.rank).all()
    
    def get_latest_by_user(self, db: Session, *, user_id: str, limit: int = 6) -> List[PathwayRecommendation]:
        """Get latest recommendations for a user"""
        return db.query(PathwayRecommendation).filter(
            PathwayRecommendation.user_id == user_id
        ).order_by(
            PathwayRecommendation.created_at.desc(),
            PathwayRecommendation.rank
        ).limit(limit).all()
    
    def create_bulk(self, db: Session, *, recommendations: List[dict], user_id: str) -> List[PathwayRecommendation]:
        """Create multiple recommendations at once"""
        db_objs = []
        for rec_data in recommendations:
            # Avoid passing user_id twice when caller already includes it in rec_data
            payload = dict(rec_data)
            payload.setdefault("user_id", user_id)
            db_obj = PathwayRecommendation(**payload)
            db.add(db_obj)
            db_objs.append(db_obj)
        db.commit()
        for obj in db_objs:
            db.refresh(obj)
        return db_objs


recommendation_crud = CRUDRecommendation(PathwayRecommendation)
