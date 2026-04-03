"""
Feedback Loop Pydantic Schemas
Models for continuous improvement feedback analytics
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class FeedbackCategory(str, Enum):
    """Category of feedback"""
    ACCURACY = "accuracy"
    USEFULNESS = "usefulness"
    RELEVANCE = "relevance"
    GENERAL = "general"


class ImprovementStatus(str, Enum):
    """Status of improvement suggestion"""
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    IMPLEMENTED = "implemented"
    DECLINED = "declined"


class DetailedFeedbackCreate(BaseModel):
    """Enhanced feedback submission for continuous improvement"""
    pathway_id: str
    recommendation_id: Optional[str] = None
    rating: int = Field(..., ge=1, le=5)
    accuracy_rating: Optional[int] = Field(None, ge=1, le=5)
    usefulness_rating: Optional[int] = Field(None, ge=1, le=5)
    is_interested: Optional[bool] = None
    feedback_text: Optional[str] = None
    category: FeedbackCategory = FeedbackCategory.GENERAL
    suggestion: Optional[str] = None
    would_recommend: Optional[bool] = None
    alternative_pathway: Optional[str] = None


class FeedbackAnalytics(BaseModel):
    """Analytics for feedback data"""
    total_feedback_count: int
    average_rating: float
    average_accuracy: Optional[float] = None
    average_usefulness: Optional[float] = None
    interest_rate: float  # percentage of users interested
    recommendation_rate: float  # percentage who would recommend
    rating_distribution: Dict[str, int]  # {"1": 5, "2": 10, ...}
    feedback_by_category: Dict[str, int]
    recent_trends: List[Dict[str, Any]]
    top_suggestions: List[str]


class PathwayFeedbackSummary(BaseModel):
    """Feedback summary for a specific pathway"""
    pathway_id: str
    pathway_title: str
    total_feedback: int
    average_rating: float
    interest_rate: float
    satisfaction_score: float
    common_feedback: List[str]
    improvement_areas: List[str]


class SystemImprovementMetrics(BaseModel):
    """Metrics showing how feedback drives system improvement"""
    total_feedback_processed: int
    recommendations_refined: int
    model_accuracy_trend: List[Dict[str, Any]]
    user_satisfaction_trend: List[Dict[str, Any]]
    active_improvements: List[Dict[str, Any]]
    last_model_update: Optional[datetime] = None
    feedback_response_rate: float


class FeedbackLoopStatus(BaseModel):
    """Status of the continuous improvement feedback loop"""
    is_active: bool = True
    total_cycles_completed: int
    current_cycle: Dict[str, Any]
    improvement_history: List[Dict[str, Any]]
    next_review_date: Optional[datetime] = None
