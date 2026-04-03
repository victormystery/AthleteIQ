"""
Feedback Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.models.base_mixins import DBModelMixin


class FeedbackBase(BaseModel):
    """Base feedback schema"""
    pathway_id: str
    rating: int = Field(..., ge=1, le=5)
    is_interested: Optional[bool] = None
    feedback_text: Optional[str] = None


class FeedbackCreate(FeedbackBase):
    """Feedback creation schema"""
    recommendation_id: Optional[str] = None


class FeedbackUpdate(BaseModel):
    """Feedback update schema"""
    rating: Optional[int] = Field(None, ge=1, le=5)
    is_interested: Optional[bool] = None
    feedback_text: Optional[str] = None


class Feedback(FeedbackBase, DBModelMixin):
    """Feedback response schema"""
    id: str
    user_id: str
    recommendation_id: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
