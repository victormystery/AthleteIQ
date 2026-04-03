"""
Progress Tracking Routes
Handles user progress on career pathways
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.models.db_schemas import (
    Progress as ProgressSchema,
    ProgressCreate,
    ProgressUpdate,
    User as UserSchema
)
from app.crud import progress_crud
from app.utils.auth import get_current_active_user

router = APIRouter(prefix="/api/progress", tags=["progress"])


@router.post("", response_model=ProgressSchema, status_code=status.HTTP_201_CREATED)
async def create_progress_entry(
    progress_data: ProgressCreate,
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a progress tracking entry for a pathway milestone
    
    Args:
        progress_data: Progress details (pathway_id, milestone, status, notes)
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Created progress record
    """
    progress = progress_crud.create(
        db,
        obj_in={
            "user_id": current_user.id,
            "pathway_id": progress_data.pathway_id,
            "milestone": progress_data.milestone,
            "status": progress_data.status,
            "notes": progress_data.notes
        }
    )
    
    return progress


@router.get("/my", response_model=List[ProgressSchema])
async def get_my_progress(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all progress entries for current user
    
    Args:
        current_user: Authenticated user
        db: Database session
        
    Returns:
        List of user's progress entries
    """
    progress = progress_crud.get_by_user(db, user_id=current_user.id)
    return progress


@router.get("/pathway/{pathway_id}", response_model=List[ProgressSchema])
async def get_pathway_progress(
    pathway_id: int,
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get progress for a specific pathway
    
    Args:
        pathway_id: Career pathway ID
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Progress entries for the pathway
    """
    progress = progress_crud.get_by_user_and_pathway(
        db,
        user_id=current_user.id,
        pathway_id=str(pathway_id)
    )
    return progress


@router.get("/stats", response_model=dict)
async def get_progress_stats(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get progress statistics for current user
    
    Args:
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Statistics about user's progress
    """
    total_progress = progress_crud.get_by_user(db, user_id=current_user.id)
    completed_count = progress_crud.get_completed_count(db, user_id=current_user.id)
    
    return {
        "total_milestones": len(total_progress),
        "completed_milestones": completed_count,
        "in_progress": len([p for p in total_progress if str(p.status) == "in_progress"]),
        "not_started": len([p for p in total_progress if str(p.status) == "not_started"])
    }


@router.put("/{progress_id}", response_model=ProgressSchema)
async def update_progress(
    progress_id: int,
    progress_data: ProgressUpdate,
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a progress entry
    
    Args:
        progress_id: Progress record ID
        progress_data: Updated progress fields
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Updated progress record
    """
    # Get existing progress
    progress = progress_crud.get(db, id=str(progress_id))
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress entry not found"
        )
    
    # Verify user owns this progress
    if str(progress.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this progress entry"
        )
    
    # Update progress
    updated_progress = progress_crud.update(
        db,
        db_obj=progress,
        obj_in=progress_data
    )
    
    return updated_progress


@router.delete("/{progress_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_progress(
    progress_id: int,
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a progress entry
    
    Args:
        progress_id: Progress record ID
        current_user: Authenticated user
        db: Database session
        
    Returns:
        No content (204)
    """
    # Get existing progress
    progress = progress_crud.get(db, id=str(progress_id))
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress entry not found"
        )
    
    # Verify user owns this progress
    if str(progress.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this progress entry"
        )
    
    # Delete progress
    progress_crud.delete(db, id=str(progress_id))
