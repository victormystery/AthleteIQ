"""
Empty utils __init__.py
"""
from app.utils.validators import (
    validate_career_interests,
    validate_rating,
    validate_participation_years,
    validate_student_data
)
from app.utils.helpers import (
    format_sport_name,
    calculate_confidence_percentage,
    format_career_name,
    get_experience_level,
    create_success_response,
    create_error_response
)
from app.utils.logger import setup_logging, get_logger
from app.utils.exceptions import (
    CareerAPIException,
    ModelLoadException,
    PredictionException,
    ValidationException,
    DataNotFoundException,
    register_exception_handlers
)

__all__ = [
    "validate_career_interests",
    "validate_rating",
    "validate_participation_years",
    "validate_student_data",
    "format_sport_name",
    "calculate_confidence_percentage",
    "format_career_name",
    "get_experience_level",
    "create_success_response",
    "create_error_response",
    "setup_logging",
    "get_logger",
    "CareerAPIException",
    "ModelLoadException",
    "PredictionException",
    "ValidationException",
    "DataNotFoundException",
    "register_exception_handlers"
]
