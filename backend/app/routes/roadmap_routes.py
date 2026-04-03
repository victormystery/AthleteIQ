"""
Roadmap Routes
API endpoints for personalized development roadmaps
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.db_schemas import User as UserSchema
from app.services.roadmap_service import roadmap_service
from app.services.roadmap_data_service import roadmap_data_service
from app.utils.auth import get_current_active_user

router = APIRouter(prefix="/api/roadmap", tags=["roadmap"])


@router.get("/pathway/{pathway_slug}")
async def get_personalized_roadmap(
    pathway_slug: str,
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Generate a personalized development roadmap for a specific career pathway.

    The roadmap is tailored based on:
    - The career pathway's requirements and progression steps
    - The user's academic profile (year of study, university, sport)
    - The user's questionnaire responses (skills, interests, motivation)
    - The user's existing progress on pathway milestones

    Args:
        pathway_slug: Career pathway identifier (e.g., 'coaching', 'sports-management')
        current_user: Authenticated user
        db: Database session

    Returns:
        PersonalizedRoadmap with steps, progress, and personalization context
    """
    roadmap = roadmap_service.generate_personalized_roadmap(
        db, user_id=current_user.id, pathway_slug=pathway_slug
    )

    if "error" in roadmap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=roadmap["error"],
        )

    return roadmap


@router.get("/summary")
async def get_roadmap_summary(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Get a summary of all personalized roadmaps for the current user.

    Returns overview of progress across all recommended pathways.

    Args:
        current_user: Authenticated user
        db: Database session

    Returns:
        RoadmapSummary with total roadmaps, progress, and pathway list
    """
    summary = roadmap_service.get_user_roadmap_summary(db, user_id=current_user.id)
    return summary


@router.post("/pathway/{pathway_slug}/progress")
async def update_roadmap_progress(
    pathway_slug: str,
    step_id: str,
    notes: Optional[str] = None,
    is_completed: bool = True,
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Update progress on a specific roadmap step.

    Creates or updates a UserProgress entry for the milestone.

    Args:
        pathway_slug: Career pathway identifier
        step_id: Roadmap step identifier
        is_completed: Whether the step is completed
        notes: Optional notes about the step
        current_user: Authenticated user
        db: Database session

    Returns:
        Updated progress entry
    """
    from app.database.models import CareerPathway
    from app.crud import progress_crud

    # Find pathway
    pathway = db.query(CareerPathway).filter(CareerPathway.slug == pathway_slug).first()
    if not pathway:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pathway '{pathway_slug}' not found",
        )

    # Check if progress entry exists for this step
    existing_progress = progress_crud.get_by_user_and_pathway(
        db, user_id=str(current_user.id), pathway_id=str(pathway.id)
    )
    existing_step = next(
        (p for p in existing_progress if str(p.milestone) == step_id), None
    )

    if existing_step:
        # Update existing
        from datetime import datetime
        update_data: dict = {
            "status": "completed" if is_completed else "in_progress",
            "notes": notes,
        }
        if is_completed:
            update_data["completed_at"] = datetime.utcnow().isoformat()
        updated = progress_crud.update(db, db_obj=existing_step, obj_in=update_data)
        return {
            "message": "Progress updated",
            "step_id": step_id,
            "status": updated.status.value if hasattr(updated.status, "value") else str(updated.status),
        }
    else:
        # Create new progress entry
        from datetime import datetime
        progress_data = {
            "user_id": current_user.id,
            "pathway_id": pathway.id,
            "milestone": step_id,
            "status": "completed" if is_completed else "in_progress",
            "notes": notes,
        }
        if is_completed:
            progress_data["completed_at"] = datetime.utcnow().isoformat()
        new_progress = progress_crud.create(db, obj_in=progress_data)
        return {
            "message": "Progress created",
            "step_id": step_id,
            "status": new_progress.status.value if hasattr(new_progress.status, "value") else str(new_progress.status),
        }


@router.get("/all")
async def get_all_roadmaps():
    """
    Get comprehensive roadmap data for all career pathways.
    
    Returns:
        Dictionary of all roadmaps with their complete steps and metadata
    """
    return roadmap_data_service.get_all_roadmaps()


@router.get("/pathways")
async def get_available_pathways():
    """
    Get list of all available career pathways with roadmap data.
    
    Returns:
        List of pathway metadata (slug, title, time to entry, cost level, total steps)
    """
    return roadmap_data_service.get_available_pathways()


@router.get("/pathway/{pathway_slug}/steps")
async def get_roadmap_steps(pathway_slug: str):
    """
    Get detailed roadmap steps for a specific career pathway.
    
    Args:
        pathway_slug: Career pathway identifier (e.g., 'professional-athlete', 'coaching')
    
    Returns:
        List of roadmap steps with details, resources, and priorities
    """
    steps = roadmap_data_service.get_roadmap_steps(pathway_slug)
    
    if not steps:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No roadmap found for pathway '{pathway_slug}'"
        )
    
    return {
        "pathway_slug": pathway_slug,
        "steps": steps,
        "total_steps": len(steps)
    }


@router.get("/pathway/{pathway_slug}/metadata")
async def get_roadmap_metadata(pathway_slug: str):
    """
    Get metadata for a specific pathway roadmap.
    
    Args:
        pathway_slug: Career pathway identifier
    
    Returns:
        Roadmap metadata including title, time to entry, cost level, and step count
    """
    metadata = roadmap_data_service.get_roadmap_metadata(pathway_slug)
    
    if not metadata:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No roadmap found for pathway '{pathway_slug}'"
        )
    
    # Add cost and duration estimates
    cost_estimate = roadmap_data_service.estimate_total_cost(pathway_slug)
    duration_estimate = roadmap_data_service.estimate_total_duration(pathway_slug)
    
    return {
        **metadata,
        "cost_estimate": cost_estimate,
        "duration_estimate": duration_estimate
    }


@router.get("/pathway/{pathway_slug}/required")
async def get_required_steps(pathway_slug: str):
    """
    Get only the required steps for a career pathway.
    
    Args:
        pathway_slug: Career pathway identifier
    
    Returns:
        List of required roadmap steps
    """
    steps = roadmap_data_service.get_required_steps(pathway_slug)
    
    return {
        "pathway_slug": pathway_slug,
        "required_steps": steps,
        "total_required": len(steps)
    }


@router.get("/pathway/{pathway_slug}/recommended")
async def get_recommended_steps(pathway_slug: str):
    """
    Get recommended (optional) steps for a career pathway.
    
    Args:
        pathway_slug: Career pathway identifier
    
    Returns:
        List of recommended roadmap steps
    """
    steps = roadmap_data_service.get_recommended_steps(pathway_slug)
    
    return {
        "pathway_slug": pathway_slug,
        "recommended_steps": steps,
        "total_recommended": len(steps)
    }


@router.get("/search")
async def search_roadmaps(q: str):
    """
    Search for career pathways by name.
    
    Args:
        q: Search query string
    
    Returns:
        List of matching pathway metadata
    """
    results = roadmap_data_service.search_roadmaps(q)
    
    return {
        "query": q,
        "results": results,
        "total_matches": len(results)
    }
