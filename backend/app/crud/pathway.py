"""
Career Pathway CRUD Operations
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.database.models import CareerPathway
from app.models.db_schemas import PathwayCreate, PathwayUpdate


class CRUDPathway(CRUDBase[CareerPathway, PathwayCreate, PathwayUpdate]):
    """CRUD operations for CareerPathway model"""
    
    def get_by_slug(self, db: Session, *, slug: str) -> Optional[CareerPathway]:
        """Get pathway by slug"""
        return db.query(CareerPathway).filter(CareerPathway.slug == slug).first()
    
    def get_by_title(self, db: Session, *, title: str) -> Optional[CareerPathway]:
        """Get pathway by title"""
        return db.query(CareerPathway).filter(CareerPathway.title == title).first()
    
    def search(self, db: Session, *, query: str) -> List[CareerPathway]:
        """Search pathways by title or description"""
        return db.query(CareerPathway).filter(
            (CareerPathway.title.ilike(f"%{query}%")) | 
            (CareerPathway.description.ilike(f"%{query}%"))
        ).all()


pathway_crud = CRUDPathway(CareerPathway)
