"""
Request and Response Models (Schemas)
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum


# Enumerations for validation
class AcademicLevel(str, Enum):
    YEAR_1 = "Year 1"
    YEAR_2 = "Year 2"
    YEAR_3 = "Year 3"
    YEAR_4 = "Year 4"
    POSTGRADUATE = "Postgraduate"
    PROFESSIONAL = "Professional / Working"


class PrimaryMotivation(str, Enum):
    COMPETITIVE = "Competition and performance"
    HEALTH = "Health and fitness"
    COACHING = "Helping or coaching others"
    ACADEMIC = "Academic or career opportunity"
    FAME = "Fame, media, or recognition"


class WorkEnvironment(str, Enum):
    FIELD_PRACTICAL = "On-field / practical"
    OFFICE = "Office / management"
    LABORATORY = "Laboratory / science / clinical"
    MEDIA = "Media / creative"
    MIXED = "A mix of environments"


# Request Models
class StudentDataRequest(BaseModel):
    """
    Student questionnaire data request
    """
    # Basic Information
    academic_level: str = Field(..., description="Current academic level")
    primary_sport: str = Field(..., description="Primary sport of interest")
    participation_years: str = Field(..., description="Years of active participation")
    participation_level: str = Field(..., description="Current participation level")
    
    # Skills & Attributes (1-5 rating)
    fitness_level: int = Field(..., ge=1, le=5, description="Physical fitness rating")
    technical_skill: int = Field(..., ge=1, le=5, description="Technical skill rating")
    leadership: int = Field(..., ge=1, le=5, description="Leadership ability rating")
    data_comfort: int = Field(..., ge=1, le=5, description="Comfort with data/analytics")
    
    # Motivation & Goals
    motivation: str = Field(..., description="PRIMARY motivation for participating")
    career_importance: str = Field(..., description="Importance of sport to career")
    work_environment: str = Field(..., description="Preferred work environment")
    
    # Challenges & History
    biggest_challenge: str = Field(..., description="Biggest challenge in pursuing sport")
    injury_history: str = Field(..., description="Sports injury history")
    
    # Career Interests & Education
    career_interests: List[str] = Field(..., description="Top 3 career interests", min_length=1, max_length=3)
    education_level: str = Field(..., description="Education commitment level")

    @validator('career_interests')
    def validate_career_interests(cls, v):
        if not v or len(v) < 1:
            raise ValueError('At least one career interest must be selected')
        if len(v) > 3:
            raise ValueError('Maximum 3 career interests allowed')
        return v

    class Config:
        schema_extra = {
            "example": {
                "academic_level": "Year 3",
                "primary_sport": "Football (Soccer)",
                "participation_years": "More than 5 years",
                "participation_level": "University/School team",
                "fitness_level": 4,
                "technical_skill": 4,
                "leadership": 5,
                "data_comfort": 3,
                "motivation": "Helping or coaching others",
                "career_importance": "Very important",
                "work_environment": "On-field / practical",
                "biggest_challenge": "Time management",
                "injury_history": "Minor (short recovery)",
                "career_interests": [
                    "Coach / Coaching education",
                    "Community sports development",
                    "Sports management / Administration"
                ],
                "education_level": "Bachelor's degree or add-on program"
            }
        }


# Response Models
class CareerOption(BaseModel):
    """Individual career pathway option"""
    rank: int = Field(..., description="Ranking position (1-6)")
    career: str = Field(..., description="Career pathway name")
    confidence: float = Field(..., ge=0, le=100, description="Confidence score percentage")
    reason: Optional[str] = Field(None, description="Reason for recommendation")
    match_score: Optional[float] = Field(None, description="Match score based on profile")
    
    # Additional fields for frontend compatibility
    pathway_id: Optional[str] = Field(None, description="Pathway database ID")
    pathway_name: Optional[str] = Field(None, description="Pathway display name")
    pathway_slug: Optional[str] = Field(None, description="Pathway URL slug")
    category: Optional[str] = Field(None, description="Pathway category")
    description: Optional[str] = Field(None, description="Pathway description")
    match_percentage: Optional[float] = Field(None, description="Match percentage")
    key_skills: Optional[List[str]] = Field(default_factory=list, description="Required skills")
    typical_salary_range: Optional[str] = Field(None, description="Salary range")
    growth_outlook: Optional[str] = Field(None, description="Job growth outlook")
    sport_specific_insights: Optional[str] = Field(None, description="Sport-specific insights")
    
    class Config:
        # Include all fields even if None, but use empty list/string for missing values
        json_encoders = {
            type(None): lambda v: v
        }


class SportInsight(BaseModel):
    """Sport-specific career insight"""
    career: str = Field(..., description="Career pathway")
    percentage: float = Field(..., description="Percentage of students choosing this path")
    popularity: str = Field(..., description="Popularity level")
    count: Optional[int] = Field(None, description="Number of students")


class SportInsights(BaseModel):
    """Sport-specific career trends"""
    has_data: bool = Field(..., description="Whether data is available")
    sport: Optional[str] = Field(None, description="Sport name")
    total_students: Optional[int] = Field(None, description="Total students in database")
    insights: Optional[List[SportInsight]] = Field(None, description="Career insights")


class CareerRequirements(BaseModel):
    """Career pathway requirements"""
    education: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    experience: Optional[str] = None


class CareerDetails(BaseModel):
    """Detailed career pathway information"""
    id: str
    title: str
    description: str
    match_score: float
    requirements: CareerRequirements
    time_to_entry: str
    cost_level: str
    average_salary: Optional[str] = None
    job_outlook: Optional[str] = None
    programs: List[str] = Field(default_factory=list)


class RecommendationResponse(BaseModel):
    """
    Main career recommendation response
    """
    primary_prediction: str = Field(..., description="Top recommended career path")
    primary_motivation: str = Field(..., description="Student's primary motivation")
    all_recommendations: List[CareerOption] = Field(..., description="All 6 recommendations")
    sport_insights: Optional[SportInsights] = Field(None, description="Sport-specific insights")
    student_profile: dict = Field(..., description="Processed student profile")
    
    class Config:
        schema_extra = {
            "example": {
                "primary_prediction": "Coaching & Development",
                "primary_motivation": "Helping or coaching others",
                "all_recommendations": [
                    {
                        "rank": 1,
                        "career": "Coaching & Development",
                        "confidence": 78.5,
                        "reason": "ML Prediction based on profile",
                        "match_score": 85.0
                    },
                    {
                        "rank": 6,
                        "career": "Coaching & Development (Youth & Community)",
                        "confidence": 58.9,
                        "reason": "Based on PRIMARY motivation: Helping or coaching others"
                    }
                ],
                "sport_insights": {
                    "has_data": True,
                    "sport": "Football",
                    "total_students": 45,
                    "insights": [
                        {
                            "career": "Coaching & Development",
                            "percentage": 42.5,
                            "popularity": "Very Popular",
                            "count": 19
                        }
                    ]
                },
                "student_profile": {}
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str = Field(..., description="Error message")
    details: Optional[str] = Field(None, description="Detailed error information")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    app: str
    version: str
    model_loaded: bool
    environment: str
