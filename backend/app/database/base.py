"""
SQLAlchemy Base Class
Import all models here for Alembic to discover them
"""
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here so Alembic can discover them
# This must be after Base is defined
def import_models():
    """Import all models for Alembic migrations"""
    from app.database.models import (
        User,
        Profile,
        CareerPathway,
        QuestionnaireResponse,
        PathwayRecommendation,
        RecommendationFeedback,
        UserProgress
    )
    return [
        User,
        Profile,
        CareerPathway,
        QuestionnaireResponse,
        PathwayRecommendation,
        RecommendationFeedback,
        UserProgress
    ]

# Import models for Alembic
import_models()
