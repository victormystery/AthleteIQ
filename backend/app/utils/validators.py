"""
Custom Validators
Additional validation logic beyond Pydantic
"""
from typing import List, Dict, Any
from fastapi import HTTPException


def validate_career_interests(interests: List[str]) -> bool:
    """
    Validate career interests selection
    Must have at least 1 and at most 3 interests
    """
    if not interests or len(interests) < 1:
        raise HTTPException(
            status_code=400,
            detail="Please select at least 1 career interest"
        )
    
    if len(interests) > 3:
        raise HTTPException(
            status_code=400,
            detail="Please select at most 3 career interests"
        )
    
    return True


def validate_rating(value: int, field_name: str) -> bool:
    """
    Validate rating values (1-5)
    """
    if value < 1 or value > 5:
        raise HTTPException(
            status_code=400,
            detail=f"{field_name} must be between 1 and 5"
        )
    return True


def validate_participation_years(years: int) -> bool:
    """
    Validate participation years
    """
    if years < 0 or years > 20:
        raise HTTPException(
            status_code=400,
            detail="Participation years must be between 0 and 20"
        )
    return True


def sanitize_input(data: str) -> str:
    """
    Sanitize user input to prevent injection attacks
    """
    # Remove any potentially dangerous characters
    dangerous_chars = ['<', '>', '{', '}', ';', '&', '|']
    for char in dangerous_chars:
        data = data.replace(char, '')
    
    return data.strip()


def validate_student_data(data: Dict[str, Any]) -> bool:
    """
    Comprehensive validation of student data
    """
    # Validate required fields
    required_fields = [
        'academic_level', 'primary_sport', 'participation_years',
        'participation_level', 'fitness_level', 'technical_skill',
        'leadership', 'data_comfort', 'motivation', 'career_importance',
        'work_environment', 'biggest_challenge', 'injury_history',
        'career_interests', 'education_level'
    ]
    
    for field in required_fields:
        if field not in data:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required field: {field}"
            )
    
    # Validate specific fields
    validate_career_interests(data['career_interests'])
    validate_participation_years(data['participation_years'])
    validate_rating(data['fitness_level'], 'fitness_level')
    validate_rating(data['technical_skill'], 'technical_skill')
    validate_rating(data['leadership'], 'leadership')
    validate_rating(data['data_comfort'], 'data_comfort')
    validate_rating(data['career_importance'], 'career_importance')
    
    return True
