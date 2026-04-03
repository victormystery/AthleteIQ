"""
Career Pathway Schemas
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.models.base_mixins import DBModelMixin


class PathwayFieldsMixin(BaseModel):
    """Common pathway fields"""
    requirements: Optional[Dict[str, Any]] = None
    education_requirements: Optional[List[str]] = None
    key_skills: Optional[List[str]] = None
    certifications: Optional[List[str]] = None


class PathwayBase(BaseModel):
    """Base pathway schema"""
    slug: str
    title: str
    description: str
    icon: str
    color: str
    work_environment: Optional[str] = None
    job_outlook: Optional[str] = None
    salary_range_min: Optional[float] = None
    salary_range_max: Optional[float] = None
    salary_currency: Optional[str] = "GBP"


class PathwayCreate(PathwayBase, PathwayFieldsMixin):
    """Pathway creation schema"""
    career_progression: Optional[List[Dict[str, Any]]] = None
    success_stories: Optional[List[Dict[str, Any]]] = None


class PathwayUpdate(PathwayFieldsMixin, BaseModel):
    """Pathway update schema - all fields optional"""
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    work_environment: Optional[str] = None
    job_outlook: Optional[str] = None
    salary_range_min: Optional[float] = None
    salary_range_max: Optional[float] = None


class Pathway(PathwayBase, PathwayFieldsMixin, DBModelMixin):
    """Pathway response schema"""
    id: str
    career_progression: Optional[List[Dict[str, Any]]] = None
    success_stories: Optional[List[Dict[str, Any]]] = None
    created_at: datetime
    updated_at: Optional[datetime]
