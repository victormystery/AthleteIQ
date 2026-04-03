"""
Helper Utilities
Common utility functions
"""
import re
from typing import List, Dict, Any
from datetime import datetime


def format_sport_name(sport: str) -> str:
    """
    Format sport name for consistency
    """
    return sport.strip().title()


def calculate_confidence_percentage(confidence: float) -> int:
    """
    Convert confidence score to percentage
    """
    return int(round(confidence * 100))


def format_career_name(career: str) -> str:
    """
    Format career name for display
    """
    return career.replace('_', ' ').title()


def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Truncate text to max length with ellipsis
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + '...'


def get_experience_level(years: int) -> str:
    """
    Categorize experience level based on years
    """
    if years < 1:
        return "Beginner"
    elif years < 3:
        return "Intermediate"
    elif years < 5:
        return "Advanced"
    else:
        return "Expert"


def get_timestamp() -> str:
    """
    Get current timestamp in ISO format
    """
    return datetime.utcnow().isoformat()


def normalize_score(score: float, min_val: float = 0, max_val: float = 1) -> float:
    """
    Normalize score to range [0, 1]
    """
    if max_val == min_val:
        return 0
    return (score - min_val) / (max_val - min_val)


def filter_unique_recommendations(recommendations: List[Dict]) -> List[Dict]:
    """
    Remove duplicate career recommendations
    """
    seen = set()
    unique = []
    
    for rec in recommendations:
        career = rec['career']
        if career not in seen:
            seen.add(career)
            unique.append(rec)
    
    return unique


def rank_recommendations(recommendations: List[Dict]) -> List[Dict]:
    """
    Rank recommendations by match score
    """
    ranked = sorted(
        recommendations,
        key=lambda x: x.get('match_score', 0),
        reverse=True
    )
    
    # Add rank numbers
    for i, rec in enumerate(ranked, 1):
        rec['rank'] = i
    
    return ranked


def merge_recommendations(
    ml_recs: List[Dict],
    motivation_rec: Dict
) -> List[Dict]:
    """
    Merge ML recommendations with motivation recommendation
    """
    # Ensure motivation rec is not duplicate
    ml_careers = {rec['career'] for rec in ml_recs}
    
    if motivation_rec['career'] in ml_careers:
        # If duplicate, just return ML recs
        return ml_recs
    
    # Otherwise, add motivation rec
    all_recs = ml_recs + [motivation_rec]
    
    # Re-rank all recommendations
    return rank_recommendations(all_recs)


def format_currency(amount: str) -> str:
    """
    Format salary string with proper currency symbols
    """
    # Already formatted in GBP
    return amount


def parse_list_string(list_str: str, delimiter: str = ',') -> List[str]:
    """
    Parse comma-separated string into list
    """
    if not list_str:
        return []
    return [item.strip() for item in list_str.split(delimiter) if item.strip()]


def create_success_response(data: Any, message: str = "Success") -> Dict:
    """
    Create standardized success response
    """
    return {
        'success': True,
        'message': message,
        'data': data,
        'timestamp': get_timestamp()
    }


def create_error_response(error: str, code: int = 500) -> Dict:
    """
    Create standardized error response
    """
    return {
        'success': False,
        'error': error,
        'code': code,
        'timestamp': get_timestamp()
    }
