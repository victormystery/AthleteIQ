"""
Roadmap Pydantic Schemas
Models for personalized development roadmaps
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class RoadmapStepType(str, Enum):
    """Type of roadmap step"""
    ACADEMIC = "academic"
    COURSE = "course"
    CERTIFICATION = "certification"
    EXPERIENCE = "experience"
    SKILL = "skill"
    NETWORKING = "networking"


class RoadmapStepPriority(str, Enum):
    """Priority level of roadmap step"""
    REQUIRED = "required"
    RECOMMENDED = "recommended"
    OPTIONAL = "optional"


class RoadmapResource(BaseModel):
    """Resource linked to a roadmap step"""
    name: str
    url: Optional[str] = None
    type: Optional[str] = None  # "video", "article", "course", "book"


class RoadmapStep(BaseModel):
    """A single step in the development roadmap"""
    id: str
    title: str
    description: str
    type: RoadmapStepType
    duration: str
    cost: str
    priority: RoadmapStepPriority
    details: List[str]
    resources: Optional[List[RoadmapResource]] = None
    order: int = 0
    is_completed: bool = False
    completion_date: Optional[datetime] = None


class PersonalizedRoadmap(BaseModel):
    """Complete personalized development roadmap"""
    pathway_id: str
    pathway_title: str
    pathway_slug: str
    student_name: Optional[str] = None
    academic_level: Optional[str] = None
    primary_sport: Optional[str] = None
    total_steps: int
    completed_steps: int = 0
    progress_percentage: float = 0.0
    estimated_duration: str
    steps: List[RoadmapStep]
    generated_at: datetime
    personalization_factors: Optional[Dict[str, Any]] = None


class RoadmapProgressUpdate(BaseModel):
    """Update progress on a roadmap step"""
    step_id: str
    is_completed: bool
    notes: Optional[str] = None


class RoadmapSummary(BaseModel):
    """Summary of user's roadmaps"""
    total_roadmaps: int
    active_roadmaps: int
    overall_progress: float
    roadmaps: List[Dict[str, Any]]
