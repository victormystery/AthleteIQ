"""
Database Pydantic Models (db_schemas.py)
Re-exports all schemas from modular files for backward compatibility
"""

# Import base mixins
from app.models.base_mixins import (
    DBModelMixin,
    ValidatedEmailMixin,
    ValidatedPasswordMixin,
    ValidatedNameMixin,
)

# Import user schemas
from app.models.user_schemas import (
    UserBase,
    UserCreate,
    UserUpdate,
    User,
    Token,
    TokenData,
    LoginRequest,
)

# Import profile schemas
from app.models.profile_schemas import (
    ProfileFieldsMixin,
    ProfileBase,
    ProfileCreate,
    ProfileUpdate,
    Profile,
    ProfileResponse,
)

# Import auth schemas
from app.models.auth_schemas import (
    RegisterRequest,
    AuthResponse,
    RegisterResponse,
    LoginResponse,
    UserInfoResponse,
)

# Import pathway schemas
from app.models.pathway_schemas import (
    PathwayFieldsMixin,
    PathwayBase,
    PathwayCreate,
    PathwayUpdate,
    Pathway,
)

# Import questionnaire schemas
from app.models.questionnaire_schemas import (
    QuestionnaireBase,
    QuestionnaireCreate,
    QuestionnaireUpdate,
    Questionnaire,
)

# Import recommendation schemas
from app.models.recommendation_schemas import (
    RecommendationBase,
    RecommendationCreate,
    RecommendationUpdate,
    Recommendation,
)

# Import feedback schemas
from app.models.feedback_schemas import (
    FeedbackBase,
    FeedbackCreate,
    FeedbackUpdate,
    Feedback,
)

# Import progress schemas
from app.models.progress_schemas import (
    ProgressBase,
    ProgressCreate,
    ProgressUpdate,
    Progress,
)

# Import roadmap schemas
from app.models.roadmap_schemas import (
    RoadmapStep,
    PersonalizedRoadmap,
    RoadmapProgressUpdate,
    RoadmapSummary,
    RoadmapResource,
)

# Import feedback loop schemas
from app.models.feedback_loop_schemas import (
    DetailedFeedbackCreate,
    FeedbackAnalytics,
    PathwayFeedbackSummary,
    SystemImprovementMetrics,
    FeedbackLoopStatus,
)

# Export all schemas for backward compatibility
__all__ = [
    # Base mixins
    "DBModelMixin",
    "ValidatedEmailMixin",
    "ValidatedPasswordMixin",
    "ValidatedNameMixin",
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "User",
    "Token",
    "TokenData",
    "LoginRequest",
    # Profile schemas
    "ProfileFieldsMixin",
    "ProfileBase",
    "ProfileCreate",
    "ProfileUpdate",
    "Profile",
    "ProfileResponse",
    # Auth schemas
    "RegisterRequest",
    "AuthResponse",
    "RegisterResponse",
    "LoginResponse",
    "UserInfoResponse",
    # Pathway schemas
    "PathwayFieldsMixin",
    "PathwayBase",
    "PathwayCreate",
    "PathwayUpdate",
    "Pathway",
    # Questionnaire schemas
    "QuestionnaireBase",
    "QuestionnaireCreate",
    "QuestionnaireUpdate",
    "Questionnaire",
    # Recommendation schemas
    "RecommendationBase",
    "RecommendationCreate",
    "RecommendationUpdate",
    "Recommendation",
    # Feedback schemas
    "FeedbackBase",
    "FeedbackCreate",
    "FeedbackUpdate",
    "Feedback",
    # Progress schemas
    "ProgressBase",
    "ProgressCreate",
    "ProgressUpdate",
    "Progress",
    # Roadmap schemas
    "RoadmapStep",
    "PersonalizedRoadmap",
    "RoadmapProgressUpdate",
    "RoadmapSummary",
    "RoadmapResource",
    # Feedback loop schemas
    "DetailedFeedbackCreate",
    "FeedbackAnalytics",
    "PathwayFeedbackSummary",
    "SystemImprovementMetrics",
    "FeedbackLoopStatus",
]
