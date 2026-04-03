"""
Feedback CRUD Operations
"""
from typing import List, Tuple, Literal
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.database.models import RecommendationFeedback
from app.models.db_schemas import FeedbackCreate, FeedbackUpdate


class CRUDFeedback(CRUDBase[RecommendationFeedback, FeedbackCreate, FeedbackUpdate]):
    """CRUD operations for RecommendationFeedback model"""
    
    def get_by_user(self, db: Session, *, user_id: str) -> List[RecommendationFeedback]:
        """Get all feedback from a user"""
        return db.query(RecommendationFeedback).filter(
            RecommendationFeedback.user_id == user_id
        ).order_by(RecommendationFeedback.created_at.desc()).all()
    
    def get_by_pathway(self, db: Session, *, pathway_id: str) -> List[RecommendationFeedback]:
        """Get all feedback for a pathway"""
        return db.query(RecommendationFeedback).filter(
            RecommendationFeedback.pathway_id == pathway_id
        ).order_by(RecommendationFeedback.created_at.desc()).all()

    def get_by_pathway_paginated(
        self,
        db: Session,
        *,
        pathway_id: str,
        page: int,
        page_size: int,
        sort_by: Literal["created_at", "rating"] = "created_at",
        sort_order: Literal["asc", "desc"] = "desc",
    ) -> Tuple[List[RecommendationFeedback], int]:
        """Get pathway feedback with pagination and sorting"""
        query = db.query(RecommendationFeedback).filter(
            RecommendationFeedback.pathway_id == pathway_id
        )

        if sort_by == "rating":
            sort_column = RecommendationFeedback.rating
        else:
            sort_column = RecommendationFeedback.created_at

        if sort_order == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        total_feedback = query.count()
        feedback_items = query.offset((page - 1) * page_size).limit(page_size).all()

        return feedback_items, total_feedback
    
    def get_average_rating(self, db: Session, *, pathway_id: str) -> float:
        """Get average rating for a pathway"""
        result = db.query(func.avg(RecommendationFeedback.rating)).filter(
            RecommendationFeedback.pathway_id == pathway_id
        ).scalar()
        return float(result) if result else 0.0


feedback_crud = CRUDFeedback(RecommendationFeedback)
