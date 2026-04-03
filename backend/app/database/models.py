"""
SQLAlchemy Database Models
"""
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Text, 
    DateTime, ForeignKey, JSON, Enum as SQLEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid
import enum

from app.database.base import Base


def generate_uuid():
    """Generate UUID for primary keys"""
    return str(uuid.uuid4())


# Enums
class UserRole(str, enum.Enum):
    """User role enumeration"""
    STUDENT = "student"
    ADMIN = "admin"
    CAREER_ADVISOR = "career_advisor"


class ProgressStatus(str, enum.Enum):
    """Progress tracking status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


# Models
class User(Base):
    """User authentication and basic info"""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)  # Nullable for OAuth users
    role = Column(SQLEnum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # OAuth fields
    oauth_provider = Column(String, nullable=True)  # 'google', 'facebook', etc.
    oauth_user_id = Column(String, nullable=True, index=True)  # Provider's user ID
    email_verified = Column(Boolean, default=False)
    avatar_url = Column(String, nullable=True)  # Profile picture URL
    
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    questionnaire_responses = relationship("QuestionnaireResponse", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("PathwayRecommendation", back_populates="user", cascade="all, delete-orphan")
    feedback = relationship("RecommendationFeedback", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")


class Profile(Base):
    """User profile information"""
    __tablename__ = "profiles"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    full_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    university = Column(String, nullable=True)
    programme_of_study = Column(String, nullable=True)
    year_of_study = Column(Integer, nullable=True)
    primary_sport = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="profile")


class CareerPathway(Base):
    """Career pathway master data"""
    __tablename__ = "career_pathways"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String, nullable=False)
    color = Column(String, nullable=False)
    
    # Details
    work_environment = Column(String, nullable=True)
    job_outlook = Column(Text, nullable=True)
    salary_range_min = Column(Float, nullable=True)
    salary_range_max = Column(Float, nullable=True)
    salary_currency = Column(String, default="GBP")
    
    # JSON fields
    requirements = Column(JSON, nullable=True)  # {education: [], skills: [], certifications: []}
    education_requirements = Column(JSON, nullable=True)  # Array of strings
    key_skills = Column(JSON, nullable=True)  # Array of strings
    certifications = Column(JSON, nullable=True)  # Array of strings
    career_progression = Column(JSON, nullable=True)  # Array of progression steps
    success_stories = Column(JSON, nullable=True)  # Array of success stories
    
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    recommendations = relationship("PathwayRecommendation", back_populates="pathway", cascade="all, delete-orphan")
    feedback = relationship("RecommendationFeedback", back_populates="pathway", cascade="all, delete-orphan")
    progress = relationship("UserProgress", back_populates="pathway", cascade="all, delete-orphan")


class QuestionnaireResponse(Base):
    """User questionnaire responses"""
    __tablename__ = "questionnaire_responses"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Questionnaire data (JSON)
    answers = Column(JSON, nullable=False)  # All 14 questionnaire fields
    
    # Status
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="questionnaire_responses")


class PathwayRecommendation(Base):
    """ML-generated career pathway recommendations for users"""
    __tablename__ = "pathway_recommendations"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    pathway_id = Column(String, ForeignKey("career_pathways.id", ondelete="CASCADE"), nullable=False)
    questionnaire_response_id = Column(String, ForeignKey("questionnaire_responses.id", ondelete="SET NULL"), nullable=True)
    
    # Recommendation details
    rank = Column(Integer, nullable=False)  # 1-6
    match_score = Column(Float, nullable=False)  # 0-100
    confidence = Column(Float, nullable=False)  # 0-100
    reason = Column(Text, nullable=True)
    is_motivation_based = Column(Boolean, default=False)
    
    # Additional metadata
    reasons = Column(JSON, nullable=True)  # Detailed reasons array
    ml_probabilities = Column(JSON, nullable=True)  # Raw ML probabilities
    
    created_at = Column(DateTime(timezone=True), default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="recommendations")
    pathway = relationship("CareerPathway", back_populates="recommendations")


class RecommendationFeedback(Base):
    """User feedback on career recommendations"""
    __tablename__ = "recommendation_feedback"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    pathway_id = Column(String, ForeignKey("career_pathways.id", ondelete="CASCADE"), nullable=False)
    recommendation_id = Column(String, ForeignKey("pathway_recommendations.id", ondelete="CASCADE"), nullable=True)
    
    # Feedback data
    rating = Column(Integer, nullable=False)  # 1-5 stars
    is_interested = Column(Boolean, nullable=True)
    feedback_text = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="feedback")
    pathway = relationship("CareerPathway", back_populates="feedback")


class UserProgress(Base):
    """Track user progress on career pathways"""
    __tablename__ = "user_progress"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    pathway_id = Column(String, ForeignKey("career_pathways.id", ondelete="CASCADE"), nullable=True)
    
    # Progress tracking
    milestone = Column(String, nullable=False)
    status = Column(SQLEnum(ProgressStatus), default=ProgressStatus.NOT_STARTED)
    notes = Column(Text, nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="progress")
    pathway = relationship("CareerPathway", back_populates="progress")
