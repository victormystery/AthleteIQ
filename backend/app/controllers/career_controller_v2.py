"""
Career Controller with Database Integration
Handles career recommendation and pathway requests with database persistence
"""
import logging
from typing import Dict, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.schemas import (
    StudentDataRequest,
    RecommendationResponse,
    CareerOption,
    SportInsights
)
from app.models.db_schemas import (
    QuestionnaireCreate,
    User,
    Pathway
)
from app.services.ml_service import ml_service
from app.services.career_analysis_service import career_analysis_service
from app.crud import (
    pathway_crud,
    questionnaire_crud,
    recommendation_crud
)

logger = logging.getLogger(__name__)


def map_ml_career_to_pathway_title(ml_career_name: str) -> str:
    """
    Map ML model career names to database pathway titles
    
    Args:
        ml_career_name: Career name returned by ML model or fallback recommendations
        
    Returns:
        Corresponding pathway title in database, or original name if no mapping exists
    """
    career_mapping = {
        'Coaching & Development': 'Coach / Coaching Education',
        'High Performance Sport': 'Professional Athlete',
        'Sports Science / Medicine': 'Sports Science / Performance Science',
        'Recreational / Fitness Industry': 'Community Sports',
        'Sports Management': 'Sports Management',  # Already matches
        'Performance Analysis': 'Sports Analytics / Performance Analysis',
        'Sports Media': 'Sports Media / Journalism',
        'Physiotherapy': 'Sports Physiotherapy',
        'Strength & Conditioning': 'Strength & Conditioning Coach',
        'Officiating': 'Officiating / Refereeing',
    }
    return career_mapping.get(ml_career_name, ml_career_name)


class CareerControllerV2:
    """
    Controller for career recommendation endpoints with database integration
    """
    
    @staticmethod
    async def get_career_recommendations_with_save(
        student_data: StudentDataRequest,
        db: Session,
        user: Optional[User] = None
    ) -> RecommendationResponse:
        """
        Process student data, return recommendations, and save to database if user is authenticated
        
        Args:
            student_data: Student questionnaire responses
            db: Database session
            user: Optional authenticated user
            
        Returns:
            RecommendationResponse with 6 recommendations and sport insights
        """
        try:
            logger.info(f"Processing career recommendations")
            
            # Convert Pydantic model to dict
            student_dict = student_data.model_dump()
            
            # Save questionnaire response if user is authenticated
            questionnaire_response = None
            if user:
                questionnaire_response = questionnaire_crud.create_or_update(
                    db,
                    obj_in={
                        "user_id": str(user.id),
                        "answers": student_dict,
                        "completed": True,
                        "completed_at": datetime.utcnow()
                    }
                )
                logger.info(f"✅ Saved/Updated questionnaire response for user: {user.email}")
            
            # Get ML-based recommendations (5 ML + 1 motivation)
            try:
                if not ml_service.is_model_loaded():
                    logger.warning("⚠️ ML model not loaded, using fallback recommendations")
                    ml_results = career_analysis_service.get_fallback_recommendations(student_dict)
                else:
                    ml_results = ml_service.get_comprehensive_recommendations(student_dict)
            except Exception as ml_error:
                logger.error(f"❌ Error in ML prediction: {ml_error}")
                logger.info("Using fallback recommendations")
                ml_results = career_analysis_service.get_fallback_recommendations(student_dict)
            
            # Get sport-specific insights
            sport_insights_dict = career_analysis_service.get_sport_insights(
                student_dict['primary_sport']
            )
            
            # Convert sport insights to Pydantic model
            sport_insights = SportInsights(**sport_insights_dict)
            
            # Enhance recommendations with detailed career information
            enhanced_recommendations_raw = career_analysis_service.enhance_recommendations_with_details(
                ml_results['all_recommendations']
            )
            
            # Save recommendations to database if user is authenticated
            if user:
                recommendations_to_save = []
                for i, rec in enumerate(enhanced_recommendations_raw[:6]):
                    # Map ML career name to database pathway title
                    ml_career_name = rec['career']
                    pathway_title = map_ml_career_to_pathway_title(ml_career_name)
                    
                    # Get or find pathway by mapped title
                    pathway = pathway_crud.get_by_title(db, title=pathway_title)
                    
                    if pathway:
                        rec_data = {
                            "user_id": str(user.id),
                            "pathway_id": str(pathway.id),
                            "questionnaire_response_id": str(questionnaire_response.id) if questionnaire_response else None,
                            "rank": i + 1,
                            "match_score": rec.get('match_score', rec.get('confidence', 0)),
                            "confidence": rec.get('confidence', 0),
                            "reason": rec.get('reason', ''),
                            "is_motivation_based": rec.get('rank', 0) == 6,
                            "ml_probabilities": ml_results.get('probabilities', {})
                        }
                        recommendations_to_save.append(rec_data)
                    else:
                        logger.warning(f"⚠️ No pathway found for '{ml_career_name}' (mapped to '{pathway_title}')")
                
                if recommendations_to_save:
                    recommendation_crud.create_bulk(db, recommendations=recommendations_to_save, user_id=str(user.id))
                    logger.info(f"✅ Saved {len(recommendations_to_save)} recommendations for user: {user.email}")
                else:
                    logger.warning(f"⚠️ No recommendations saved - no matching pathways found")
            
            # Convert to CareerOption models with full pathway information
            enhanced_recommendations = []
            for rec in enhanced_recommendations_raw[:6]:
                score_value = float(rec.get('match_score', rec.get('confidence', 0)))
                confidence_value = float(rec.get('confidence', 0))
                score_1dp = round(score_value, 1)
                confidence_1dp = round(confidence_value, 1)

                # Map ML career name to database pathway title
                ml_career_name = rec['career']
                pathway_title = map_ml_career_to_pathway_title(ml_career_name)
                
                # Get pathway details from database using mapped title
                pathway = pathway_crud.get_by_title(db, title=pathway_title)
                details = rec.get('details', {})
                
                # Safely extract key_skills
                key_skills = []
                if details and 'requirements' in details:
                    key_skills = details.get('requirements', {}).get('skills', [])
                elif pathway and pathway.key_skills:
                    # key_skills is a JSON field, ensure it's a list
                    if isinstance(pathway.key_skills, list):
                        key_skills = pathway.key_skills
                
                career_option = {
                    "rank": rec.get('rank', 0),
                    "career": rec['career'],
                    "confidence": confidence_1dp,
                    "reason": rec.get('reason', ''),
                    "match_score": score_1dp,
                    # Additional fields for frontend
                    "pathway_id": str(pathway.id) if pathway else details.get('id', rec['career'].lower().replace(' ', '_')),
                    "pathway_name": rec['career'],
                    "pathway_slug": pathway.slug if pathway else details.get('id', rec['career'].lower().replace(' ', '-').replace('/', '-')),
                    "category": "Sports Career",
                    "description": details.get('description', '') or (pathway.description if pathway else ''),
                    "match_percentage": score_1dp,
                    "key_skills": key_skills,
                    "typical_salary_range": details.get('average_salary', ''),
                    "growth_outlook": details.get('job_outlook', '') or (pathway.job_outlook if pathway else ''),
                    "sport_specific_insights": rec.get('reason', '')
                }
                enhanced_recommendations.append(CareerOption(**career_option))
            
            
            # Create student profile summary
            student_profile = {
                'academic_level': student_dict['academic_level'],
                'primary_sport': student_dict['primary_sport'],
                'participation_years': student_dict['participation_years'],
                'participation_level': student_dict['participation_level'],
                'fitness_level': student_dict['fitness_level'],
                'technical_skill': student_dict['technical_skill'],
                'leadership': student_dict['leadership'],
                'primary_motivation': student_dict['motivation'],
                'career_interests': student_dict['career_interests']
            }
            
            # Build response
            response = RecommendationResponse(
                primary_prediction=ml_results['primary_prediction'],
                primary_motivation=student_dict['motivation'],
                all_recommendations=enhanced_recommendations,
                sport_insights=sport_insights,
                student_profile=student_profile
            )
            
            logger.info(f"Successfully generated {len(response.all_recommendations)} recommendations")
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate career recommendations: {str(e)}"
            )
    
    @staticmethod
    async def get_user_recommendations(user: User, db: Session) -> Dict:
        """
        Get saved recommendations for authenticated user
        
        Args:
            user: Authenticated user
            db: Database session
            
        Returns:
            User's saved recommendations
        """
        try:
            recommendations = recommendation_crud.get_latest_by_user(db, user_id=user.id, limit=6)
            
            # Serialize recommendations properly
            serialized_recs = []
            for rec in recommendations:
                pathway = rec.pathway if hasattr(rec, 'pathway') and rec.pathway else pathway_crud.get(db, id=rec.pathway_id)
                pathway_slug = pathway.slug if pathway and getattr(pathway, 'slug', None) else str(rec.pathway_id)
                pathway_title = pathway.title if pathway and getattr(pathway, 'title', None) else str(rec.pathway_id)

                serialized_recs.append({
                    "id": str(rec.id),
                    "pathway_id": str(rec.pathway_id),
                    "pathway_slug": pathway_slug,
                    "rank": rec.rank,
                    "match_score": rec.match_score,
                    "confidence": rec.confidence,
                    "reason": rec.reason,
                    "is_motivation_based": rec.is_motivation_based,
                    "created_at": rec.created_at.isoformat() if rec.created_at else None,
                    "pathway": {
                        "title": pathway_title,
                        "name": pathway_title,
                        "slug": pathway_slug
                    }
                })
            
            return {
                "success": True,
                "total": len(serialized_recs),
                "recommendations": serialized_recs
            }
            
        except Exception as e:
            logger.error(f"Error fetching user recommendations: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch recommendations: {str(e)}"
            )
    
    @staticmethod
    async def get_user_assessment_history(user: User, db: Session) -> Dict:
        """
        Get complete assessment history including questionnaires and recommendations
        
        Args:
            user: Authenticated user
            db: Database session
            
        Returns:
            User's assessment history with questionnaires and their recommendations
        """
        try:
            from app.crud import questionnaire_crud
            
            # Get all questionnaires
            questionnaires = questionnaire_crud.get_by_user(db, user_id=user.id)
            
            # Get all recommendations grouped by questionnaire_response_id
            all_recommendations = recommendation_crud.get_by_user(db, user_id=user.id)
            
            # Build history entries
            history = []
            for questionnaire in questionnaires:
                # Find recommendations for this questionnaire and serialize pathway safely.
                recs = []
                for rec in all_recommendations:
                    if rec.questionnaire_response_id != str(questionnaire.id):
                        continue

                    pathway = rec.pathway if hasattr(rec, "pathway") and rec.pathway else pathway_crud.get(db, id=rec.pathway_id)
                    pathway_slug = pathway.slug if pathway and getattr(pathway, "slug", None) else str(rec.pathway_id)
                    pathway_title = pathway.title if pathway and getattr(pathway, "title", None) else str(rec.pathway_id)

                    recs.append({
                        "id": str(rec.id),
                        "pathway_id": str(rec.pathway_id),
                        "pathway": {
                            "id": str(pathway.id) if pathway and getattr(pathway, "id", None) else str(rec.pathway_id),
                            "title": pathway_title,
                            "name": pathway_title,
                            "slug": pathway_slug,
                        },
                        "rank": rec.rank,
                        "match_score": rec.match_score,
                        "confidence": rec.confidence,
                        "reason": rec.reason,
                        "is_motivation_based": rec.is_motivation_based,
                    })
                
                history.append({
                    "questionnaire_id": str(questionnaire.id),
                    "completed_at": questionnaire.completed_at or questionnaire.created_at,
                    "answers": questionnaire.answers,
                    "completed": questionnaire.completed,
                    "recommendations": recs[:6]  # Top 6 recommendations
                })
            
            # Sort by date (most recent first)
            history.sort(key=lambda x: x["completed_at"], reverse=True)
            
            return {
                "success": True,
                "total_assessments": len(history),
                "history": history
            }
            
        except Exception as e:
            logger.error(f"Error fetching user assessment history: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch assessment history: {str(e)}"
            )
    
    @staticmethod
    async def get_career_pathways(db: Session) -> Dict:
        """
        Get all available career pathway details from database
        
        Args:
            db: Database session
            
        Returns:
            Dictionary of all career pathways with details
        """
        try:
            pathways = pathway_crud.get_multi(db, skip=0, limit=100)
            # Convert SQLAlchemy models to Pydantic schemas
            pathway_schemas = [Pathway.model_validate(p) for p in pathways]
            return {
                'success': True,
                'total_pathways': len(pathway_schemas),
                'pathways': pathway_schemas
            }
        except Exception as e:
            logger.error(f"Error fetching career pathways: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch career pathways: {str(e)}"
            )
    
    @staticmethod
    async def get_career_pathway_by_slug(slug: str, db: Session) -> Dict:
        """
        Get specific career pathway details by slug
        
        Args:
            slug: Career pathway slug
            db: Database session
            
        Returns:
            Career pathway details
        """
        try:
            pathway = pathway_crud.get_by_slug(db, slug=slug)
            
            if not pathway:
                raise HTTPException(
                    status_code=404,
                    detail=f"Career pathway '{slug}' not found"
                )
            
            # Convert SQLAlchemy model to Pydantic schema
            pathway_schema = Pathway.model_validate(pathway)
            return {
                'success': True,
                'pathway': pathway_schema
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error fetching pathway {slug}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch career pathway: {str(e)}"
            )
    
    @staticmethod
    async def get_sport_insights(sport: str) -> Dict:
        """
        Get sport-specific career insights
        
        Args:
            sport: Sport name
            
        Returns:
            Sport-specific career preferences and statistics
        """
        try:
            insights = career_analysis_service.get_sport_insights(sport)
            return {
                'success': True,
                'insights': insights
            }
        except Exception as e:
            logger.error(f"Error fetching sport insights for {sport}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch sport insights: {str(e)}"
            )


career_controller_v2 = CareerControllerV2()
