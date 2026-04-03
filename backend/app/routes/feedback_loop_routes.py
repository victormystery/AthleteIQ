"""
Feedback Loop Routes
API endpoints for continuous improvement feedback analytics
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.db_schemas import (
    User as UserSchema,
    FeedbackCreate,
    Feedback as FeedbackSchema,
)
from app.crud import feedback_crud
from app.services.feedback_loop_service import feedback_loop_service
from app.utils.auth import get_current_active_user

router = APIRouter(prefix="/api/feedback-loop", tags=["feedback-loop"])


@router.post("/submit", response_model=FeedbackSchema, status_code=status.HTTP_201_CREATED)
async def submit_detailed_feedback(
    feedback_data: FeedbackCreate,
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Submit detailed feedback for a career pathway recommendation.
    This feeds into the continuous improvement loop.

    Args:
        feedback_data: Feedback details (pathway_id, rating, is_interested, feedback_text)
        current_user: Authenticated user
        db: Database session

    Returns:
        Created feedback record
    """
    feedback = feedback_crud.create(
        db,
        obj_in={
            "user_id": current_user.id,
            "pathway_id": feedback_data.pathway_id,
            "recommendation_id": feedback_data.recommendation_id,
            "rating": feedback_data.rating,
            "is_interested": feedback_data.is_interested,
            "feedback_text": feedback_data.feedback_text,
        },
    )
    return feedback


@router.get("/analytics")
async def get_feedback_analytics(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get comprehensive feedback analytics across all pathways.

    Returns:
        FeedbackAnalytics with ratings, trends, and distributions
    """
    analytics = feedback_loop_service.get_feedback_analytics(db)
    return analytics


@router.get("/pathway/{pathway_id}/summary")
async def get_pathway_feedback_summary(
    pathway_id: str,
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get feedback summary for a specific career pathway.

    Args:
        pathway_id: Career pathway ID

    Returns:
        PathwayFeedbackSummary with ratings, interest rate, and common feedback
    """
    summary = feedback_loop_service.get_pathway_feedback_summary(db, pathway_id=pathway_id)
    return summary


@router.get("/improvements")
async def get_system_improvements(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get system improvement metrics showing how feedback drives continuous improvement.

    Returns:
        SystemImprovementMetrics with trends, active improvements, and response rates
    """
    metrics = feedback_loop_service.get_system_improvement_metrics(db)
    return metrics


@router.get("/status")
async def get_feedback_loop_status(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get the current status of the continuous improvement feedback loop.

    Returns:
        FeedbackLoopStatus with cycle progress and improvement history
    """
    loop_status = feedback_loop_service.get_feedback_loop_status(db)
    return loop_status


@router.get("/my-impact")
async def get_my_feedback_impact(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Show the current user how their feedback has contributed to system improvement.

    Returns:
        User's feedback impact summary with badges and contribution history
    """
    impact = feedback_loop_service.get_user_feedback_impact(
        db, user_id=current_user.id
    )
    return impact
