"""
Career Recommendation Routes (Database-backed)
Handles career recommendations with database persistence
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database.session import get_db
from app.models.schemas import StudentDataRequest, RecommendationResponse
from app.models.db_schemas import User as UserSchema
from app.controllers.career_controller_v2 import career_controller_v2
from app.utils.auth import get_current_user_optional, get_current_active_user

router = APIRouter(prefix="/api/career", tags=["career"])


@router.post("/predict")
async def predict_career(
    student_data: StudentDataRequest,
    db: Session = Depends(get_db),
    current_user: Optional[UserSchema] = Depends(get_current_user_optional)
):
    """
    Get career recommendations based on student questionnaire data
    Saves to database if user is authenticated, otherwise returns anonymous recommendations
    
    Args:
        student_data: Student questionnaire responses (14 fields)
        db: Database session
        current_user: Optional authenticated user (JWT token)
        
    Returns:
        6 career recommendations with sport-specific insights (frontend-compatible format)
    """
    result = await career_controller_v2.get_career_recommendations_with_save(
        student_data=student_data,
        db=db,
        user=current_user
    )
    
    # Serialize recommendations properly
    serialized_recommendations = [
        rec.dict(exclude_none=False) for rec in result.all_recommendations
    ]
    
    # Transform to frontend-expected format
    return {
        "success": True,
        "message": "Recommendations generated successfully",
        "recommendations": serialized_recommendations,
        "total_recommendations": len(serialized_recommendations),
        "user_id": str(current_user.id) if current_user else None,
        "recommendation_id": None  # Will be added when saving feedback
    }


@router.get("/recommendations", response_model=dict)
async def get_my_recommendations(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get saved recommendations for authenticated user
    
    Args:
        current_user: Authenticated user
        db: Database session
        
    Returns:
        User's saved recommendations
    """
    return await career_controller_v2.get_user_recommendations(
        user=current_user,
        db=db
    )


@router.get("/history", response_model=dict)
async def get_my_assessment_history(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get complete assessment history including questionnaires and recommendations
    
    Args:
        current_user: Authenticated user
        db: Database session
        
    Returns:
        User's assessment history with questionnaires and recommendations
    """
    return await career_controller_v2.get_user_assessment_history(
        user=current_user,
        db=db
    )


@router.get("/pathways", response_model=dict)
async def get_all_pathways(
    db: Session = Depends(get_db)
):
    """
    Get all available career pathways from database
    
    Args:
        db: Database session
        
    Returns:
        List of all career pathways with details
    """
    return await career_controller_v2.get_career_pathways(db=db)


@router.get("/pathways/{slug}", response_model=dict)
async def get_pathway_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    """
    Get specific career pathway by slug
    
    Args:
        slug: Career pathway slug (e.g., 'coaching-development')
        db: Database session
        
    Returns:
        Career pathway details
    """
    return await career_controller_v2.get_career_pathway_by_slug(
        slug=slug,
        db=db
    )


@router.get("/sports/{sport}/insights", response_model=dict)
async def get_sport_specific_insights(sport: str):
    """
    Get career insights specific to a sport
    
    Args:
        sport: Sport name (e.g., 'Football')
        
    Returns:
        Sport-specific career preferences and statistics
    """
    return await career_controller_v2.get_sport_insights(sport=sport)
