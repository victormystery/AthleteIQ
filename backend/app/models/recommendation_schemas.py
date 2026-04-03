"""
Recommendation Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.models.base_mixins import DBModelMixin
from app.models.pathway_schemas import Pathway


class RecommendationBase(BaseModel):
    """Base recommendation schema"""
    pathway_id: str
    rank: int = Field(..., ge=1, le=6)
    match_score: float = Field(..., ge=0, le=100)
    confidence: float = Field(..., ge=0, le=100)
    reason: Optional[str] = None
    is_motivation_based: bool = False


class RecommendationCreate(RecommendationBase):
    """Recommendation creation schema"""
    questionnaire_response_id: Optional[str] = None
    reasons: Optional[List[str]] = None
    ml_probabilities: Optional[Dict[str, float]] = None


class RecommendationUpdate(BaseModel):
    """Recommendation update schema"""
    match_score: Optional[float] = Field(None, ge=0, le=100)
    confidence: Optional[float] = Field(None, ge=0, le=100)
    reason: Optional[str] = None


class Recommendation(RecommendationBase, DBModelMixin):
    """Recommendation response schema"""
    id: str
    user_id: str
    questionnaire_response_id: Optional[str]
    reasons: Optional[List[str]] = None
    ml_probabilities: Optional[Dict[str, float]] = None
    created_at: datetime
    pathway: Optional[Pathway] = None
