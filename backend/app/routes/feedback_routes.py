"""
Feedback Management Routes
Handles pathway recommendation feedback
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.models.db_schemas import (
    Feedback as FeedbackSchema,
    FeedbackCreate,
    FeedbackUpdate,
    User as UserSchema
)
from app.crud import feedback_crud
from app.utils.auth import get_current_active_user

router = APIRouter(prefix="/api/feedback", tags=["feedback"])


@router.post("", response_model=FeedbackSchema, status_code=status.HTTP_201_CREATED)
async def submit_feedback(
    feedback_data: FeedbackCreate,
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Submit feedback for a career pathway recommendation
    
    Args:
        feedback_data: Feedback details (recommendation_id, rating, is_interested, feedback_text)
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
            "feedback_text": feedback_data.feedback_text
        }
    )
    
    return feedback


@router.get("/my", response_model=List[FeedbackSchema])
async def get_my_feedback(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all feedback submitted by current user
    
    Args:
        current_user: Authenticated user
        db: Database session
        
    Returns:
        List of user's feedback
    """
    feedback = feedback_crud.get_by_user(db, user_id=current_user.id)
    return feedback


@router.get("/my-feedback", response_model=dict)
async def get_my_feedback_legacy(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all feedback submitted by current user in legacy object format.

    Returns:
        Object containing user's feedback list
    """
    feedback = feedback_crud.get_by_user(db, user_id=current_user.id)
    return {"feedback": feedback}


@router.get("/pathway/{pathway_id}", response_model=dict)
async def get_pathway_feedback(
    pathway_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all feedback for a specific pathway with average rating
    
    Args:
        pathway_id: Career pathway ID
        db: Database session
        
    Returns:
        Pathway feedback and statistics
    """
    feedback_list = feedback_crud.get_by_pathway(db, pathway_id=pathway_id)
    average_rating = feedback_crud.get_average_rating(db, pathway_id=pathway_id)
    
    return {
        "pathway_id": pathway_id,
        "total_feedback": len(feedback_list),
        "average_rating": average_rating,
        "feedback": feedback_list
    }


@router.get("/pathway/{pathway_id}/feedback", response_model=dict)
async def get_pathway_feedback_by_pathway(
    pathway_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort_by: str = Query("created_at", pattern="^(created_at|rating)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """
    Get feedback for a specific pathway.

    Args:
        pathway_id: Career pathway ID
        db: Database session

    Returns:
        Pathway feedback and statistics
    """
    feedback_list, total_feedback = feedback_crud.get_by_pathway_paginated(
        db,
        pathway_id=pathway_id,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    average_rating = feedback_crud.get_average_rating(db, pathway_id=pathway_id)
    total_pages = (total_feedback + page_size - 1) // page_size if total_feedback > 0 else 0

    return {
        "pathway_id": pathway_id,
        "total_feedback": total_feedback,
        "average_rating": average_rating,
        "feedback": feedback_list,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        },
        "sorting": {
            "sort_by": sort_by,
            "sort_order": sort_order,
        },
    }


@router.put("/{feedback_id}", response_model=FeedbackSchema)
async def update_feedback(
    feedback_id: str,
    feedback_data: FeedbackUpdate,
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update existing feedback
    
    Args:
        feedback_id: Feedback record ID
        feedback_data: Updated feedback fields
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Updated feedback record
    """
    # Get existing feedback
    feedback = feedback_crud.get(db, id=feedback_id)
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    # Verify user owns this feedback through recommendation
    if feedback.recommendation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this feedback"
        )
    
    # Update feedback
    updated_feedback = feedback_crud.update(
        db,
        db_obj=feedback,
        obj_in=feedback_data
    )
    
    return updated_feedback
