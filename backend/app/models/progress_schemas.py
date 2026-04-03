"""
Progress Schemas
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.base_mixins import DBModelMixin


class ProgressBase(BaseModel):
    """Base progress schema"""
    pathway_id: Optional[str] = None
    milestone: str
    status: str = "not_started"
    notes: Optional[str] = None


# ProgressCreate is same as Base
ProgressCreate = ProgressBase


class ProgressUpdate(BaseModel):
    """Progress update schema"""
    status: Optional[str] = None
    notes: Optional[str] = None
    completed_at: Optional[datetime] = None


class Progress(ProgressBase, DBModelMixin):
    """Progress response schema"""
    id: str
    user_id: str
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
