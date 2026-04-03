"""
Questionnaire Management Routes
Handles saving and retrieving questionnaire responses with ML analysis
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import logging

from app.database.session import get_db
from app.models.db_schemas import (
    Questionnaire as QuestionnaireSchema,
    QuestionnaireCreate,
    User as UserSchema
)
from app.crud import questionnaire_crud
from app.utils.auth import get_current_active_user, get_current_user_optional
from app.services.ml_service import ml_service
from app.services.google_sheets_service import get_sheets_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/questionnaire", tags=["questionnaire"])


@router.post("", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
async def save_questionnaire(
    questionnaire_data: QuestionnaireCreate,
    db: Session = Depends(get_db),
    current_user: Optional[UserSchema] = Depends(get_current_user_optional)
):
    """
    Save questionnaire response with ML analysis and Google Sheets integration
    
    This endpoint:
    1. Analyzes the questionnaire using the trained ML model
    2. Saves the questionnaire to the database
    3. Writes the results to Google Sheets (if configured)
    
    Args:
        questionnaire_data: Questionnaire responses
        db: Database session
        current_user: Optional authenticated user
        
    Returns:
        Saved questionnaire and ML predictions
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to save questionnaire"
        )
    
    try:
        # 1. Get ML predictions using the training data
        logger.info(f"Analyzing questionnaire for user: {current_user.email}")
        
        ml_predictions = None
        if ml_service.is_model_loaded():
            try:
                # Get comprehensive career recommendations
                ml_predictions = ml_service.get_comprehensive_recommendations(
                    questionnaire_data.answers
                )
                logger.info(f"✅ ML predictions generated: {ml_predictions['primary_prediction']}")
            except Exception as e:
                logger.error(f"❌ Error generating ML predictions: {e}")
                # Continue without ML predictions
        else:
            logger.warning("⚠️ ML model not loaded. Saving questionnaire without predictions.")
        
        # 2. Save to database
        questionnaire = questionnaire_crud.create_or_update(
            db,
            obj_in={
                "user_id": current_user.id,
                "answers": questionnaire_data.answers,
                "completed": questionnaire_data.completed
            }
        )
        logger.info(f"✅ Questionnaire saved/updated in database: {questionnaire.id}")
        
        # 3. Write to Google Sheets (non-blocking, won't fail the request)
        sheets_service = get_sheets_service()
        if sheets_service.is_initialized():
            try:
                sheets_result = sheets_service.append_questionnaire_result(
                    user_email=current_user.email,
                    questionnaire_data=questionnaire_data.answers,
                    ml_predictions=ml_predictions
                )
                if sheets_result:
                    logger.info(f"✅ Results saved to Google Sheets for {current_user.email}")
                else:
                    logger.warning("⚠️ Failed to save to Google Sheets (non-critical)")
            except Exception as e:
                logger.error(f"❌ Error writing to Google Sheets: {e}")
                # Non-critical error, continue
        else:
            logger.info("ℹ️ Google Sheets integration not configured")
        
        # 4. Return response with questionnaire and predictions
        return {
            "questionnaire": {
                "id": questionnaire.id,
                "user_id": questionnaire.user_id,
                "answers": questionnaire.answers,
                "completed": questionnaire.completed,
                "completed_at": questionnaire.completed_at,
                "created_at": questionnaire.created_at,
                "updated_at": questionnaire.updated_at
            },
            "ml_predictions": ml_predictions,
            "saved_to_sheets": sheets_service.is_initialized()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error saving questionnaire: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving questionnaire: {str(e)}"
        )


@router.get("/latest", response_model=QuestionnaireSchema)
async def get_latest_questionnaire(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get user's most recent questionnaire response
    
    Args:
        current_user: Authenticated user
        db: Database session
        
    Returns:
        Latest questionnaire response
    """
    questionnaire = questionnaire_crud.get_latest_by_user(db, user_id=current_user.id)
    
    if not questionnaire:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No questionnaire found for this user"
        )
    
    return questionnaire


@router.get("/history", response_model=List[QuestionnaireSchema])
async def get_questionnaire_history(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all questionnaire responses for user
    
    Args:
        current_user: Authenticated user
        db: Database session
        
    Returns:
        List of all questionnaires
    """
    questionnaires = questionnaire_crud.get_by_user(db, user_id=current_user.id)
    return questionnaires


@router.get("/completed", response_model=List[QuestionnaireSchema])
async def get_completed_questionnaires(
    current_user: UserSchema = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get only completed questionnaire responses
    
    Args:
        current_user: Authenticated user
        db: Database session
        
    Returns:
        List of completed questionnaires
    """
    questionnaires = questionnaire_crud.get_completed_by_user(db, user_id=current_user.id)
    return questionnaires
