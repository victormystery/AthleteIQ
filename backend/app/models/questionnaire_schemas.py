"""
Questionnaire Schemas
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

from app.models.base_mixins import DBModelMixin


class QuestionnaireBase(BaseModel):
    """Base questionnaire schema"""
    answers: Dict[str, Any]
    completed: bool = False


# QuestionnaireCreate is same as Base
QuestionnaireCreate = QuestionnaireBase


class QuestionnaireUpdate(BaseModel):
    """Questionnaire update schema"""
    answers: Optional[Dict[str, Any]] = None
    completed: Optional[bool] = None
    completed_at: Optional[datetime] = None


class Questionnaire(QuestionnaireBase, DBModelMixin):
    """Questionnaire response schema"""
    id: str
    user_id: str
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
