"""
Machine Learning Service
Handles ML model loading, predictions, and recommendations
"""
import joblib
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import logging
from app.config.settings import get_settings

logger = logging.getLogger(__name__)


class MLService:
    """
    Service for handling ML model operations
    Based on the Random Forest model trained in the Jupyter notebook
    """
    
    def __init__(self):
        self.pipeline: Optional[Any] = None
        self.classes: Optional[np.ndarray] = None
        self.feature_names: Optional[List[str]] = None
        self.model: Optional[Any] = None
        self._load_model()
    
    def _load_model(self):
        """Load the trained ML model"""
        try:
            settings = get_settings()
            logger.info(f"Loading ML model from: {settings.MODEL_PATH}")
            self.pipeline = joblib.load(settings.MODEL_PATH)
            if self.pipeline is not None:
                self.model = self.pipeline.named_steps['model']
                if self.model is not None:
                    self.classes = self.model.classes_
                    logger.info(f"✅ Model loaded successfully")
                    if self.classes is not None:
                        logger.info(f"📊 Career pathways: {list(self.classes)}")
        except FileNotFoundError:
            settings = get_settings()
            logger.warning(f"⚠️ Model file not found at: {settings.MODEL_PATH}")
            logger.info("System will use fallback rule-based recommendations")
            self.pipeline = None
            self.model = None
            self.classes = None
        except Exception as e:
            logger.error(f"❌ Error loading model: {e}")
            logger.info("System will use fallback rule-based recommendations")
            self.pipeline = None
            self.model = None
            self.classes = None
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.pipeline is not None
    
    def prepare_student_data(self, student_data: dict) -> pd.DataFrame:
        """
        Convert student data to DataFrame format expected by the model
        Maps frontend field names to model feature names
        """
        # Map frontend names to model feature names
        model_data = {
            'academic_level': str(student_data.get('academic_level', '')),
            'primary_sport': str(student_data.get('primary_sport', '')),
            'experience_years': str(student_data.get('participation_years', '')),  # Map participation_years to experience_years
            'participation_level': str(student_data.get('participation_level', '')),
            # Keep all inputs as strings to match training-time dtype handling
            'fitness': str(student_data.get('fitness_level', '3')),
            'technical_skill': str(student_data.get('technical_skill', '3')),
            'leadership': str(student_data.get('leadership', '3')),
            'data_comfort': str(student_data.get('data_comfort', '3')),
            'primary_motivation': str(student_data.get('motivation', '')),  # Map motivation to primary_motivation
            'career_importance': str(student_data.get('career_importance', '')),
            'work_environment': str(student_data.get('work_environment', '')),
            'biggest_challenge': str(student_data.get('biggest_challenge', '')),
            'injury_history': str(student_data.get('injury_history', '')),
            'education_commitment': str(student_data.get('education_level', ''))  # Map education_level to education_commitment
        }
        
        return pd.DataFrame([model_data])
    
    def get_ml_predictions(self, student_df: pd.DataFrame) -> Tuple[str, np.ndarray, np.ndarray]:
        """
        Get ML predictions from the Random Forest model
        
        Returns:
            - primary_prediction: Top predicted career
            - probabilities: Probability scores for all careers
            - sorted_indices: Indices sorted by probability
        """
        if self.pipeline is None:
            raise Exception("ML model not loaded")
            
        prediction = self.pipeline.predict(student_df)[0]
        probabilities = self.pipeline.predict_proba(student_df)[0]
        sorted_indices = np.argsort(probabilities)[::-1]
        
        return prediction, probabilities, sorted_indices
    
    def create_ml_recommendations(
        self, 
        probabilities: np.ndarray, 
        sorted_indices: np.ndarray
    ) -> List[Dict]:
        """
        Create 5 ML-based recommendations from model predictions
        """
        if self.classes is None:
            raise Exception("ML model not loaded properly")
            
        recommendations = []
        settings = get_settings()
        for i in range(min(settings.ML_RECOMMENDATIONS, len(self.classes))):
            idx = sorted_indices[i]
            recommendations.append({
                'rank': i + 1,
                'career': str(self.classes[idx]),
                'confidence': float(probabilities[idx] * 100),
                'reason': 'ML Prediction based on profile'
            })
        
        return recommendations
    
    def create_motivation_recommendation(
        self,
        primary_motivation: str,
        probabilities: np.ndarray,
        sorted_indices: np.ndarray
    ) -> Dict:
        """
        Create the 6th recommendation based on PRIMARY motivation
        This aligns with the notebook's focus on motivation-driven recommendations
        """
        if self.classes is None:
            raise Exception("ML model not loaded properly")
            
        # Motivation-to-Career mapping from notebook analysis
        motivation_career_map = {
            'Competition and performance': 'High Performance Sport (Elite Athlete Track)',
            'Health and fitness': 'Recreational/Fitness Industry (Wellness Focus)',
            'Helping or coaching others': 'Coaching & Development (Youth & Community)',
            'Academic or career opportunity': 'Sports Science/Medicine (Research & Innovation)',
            'Fame, media, or recognition': 'Sports Management (Event & Community Sport)',
        }
        
        # Get motivation-aligned career or fallback to lowest ML prediction
        motivation_rec = motivation_career_map.get(
            primary_motivation,
            str(self.classes[sorted_indices[-1]])
        )
        
        # Calculate weighted confidence (75% of top prediction)
        weighted_confidence = float(probabilities[sorted_indices[0]] * 75)
        
        return {
            'rank': 6,
            'career': motivation_rec,
            'confidence': weighted_confidence,
            'reason': f'Based on PRIMARY motivation: {primary_motivation}'
        }
    
    def get_comprehensive_recommendations(
        self,
        student_data: dict
    ) -> Dict:
        """
        Main method to generate all 6 career recommendations
        Combines ML predictions with motivation-based recommendation
        """
        # Prepare data
        student_df = self.prepare_student_data(student_data)
        
        # Get ML predictions
        primary_prediction, probabilities, sorted_indices = self.get_ml_predictions(student_df)
        
        # Create 5 ML-based recommendations
        ml_recommendations = self.create_ml_recommendations(probabilities, sorted_indices)
        
        # Create 6th motivation-based recommendation
        motivation_rec = self.create_motivation_recommendation(
            student_data['motivation'],
            probabilities,
            sorted_indices
        )
        
        # Combine all recommendations
        all_recommendations = ml_recommendations + [motivation_rec]
        
        return {
            'primary_prediction': str(primary_prediction),
            'all_recommendations': all_recommendations,
            'probabilities': probabilities.tolist(),
            'classes': self.classes.tolist() if self.classes is not None else []
        }
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance from the Random Forest model"""
        if self.pipeline is None or self.model is None:
            return {}
            
        try:
            model = self.pipeline.named_steps['model']
            preprocessor = self.pipeline.named_steps['preprocessor']
            
            # Get feature names after preprocessing
            feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out()
            importances = model.feature_importances_
            
            # Create feature importance dictionary
            importance_dict = dict(zip(feature_names, importances))
            
            # Sort by importance
            sorted_importance = dict(
                sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
            )
            
            return sorted_importance
        except Exception as e:
            logger.error(f"Error getting feature importance: {e}")
            return {}


# Singleton instance
ml_service = MLService()
