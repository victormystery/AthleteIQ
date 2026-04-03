"""
Google Sheets Service
Handles writing questionnaire results to Google Sheets
"""
import gspread
from gspread import Worksheet, Spreadsheet
from gspread.utils import ValueInputOption
from google.oauth2.service_account import Credentials
from typing import Dict, Any, List, Optional, cast
import logging
from datetime import datetime
import os
import json

logger = logging.getLogger(__name__)


class GoogleSheetsService:
    """
    Service for writing questionnaire data to Google Sheets
    """
    
    def __init__(self):
        self.client: Optional[gspread.Client] = None
        self.spreadsheet_id = "1tT91nRZYuYtJ6EWUa51q1OuzyUPHpox4QVb8TMqa-r0"
        self.worksheet_name = "Form Responses 1"
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Google Sheets client with service account credentials"""
        try:
            # Define the scopes
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Get credentials from settings (which loads from .env)
            try:
                from app.config.settings import get_settings
                settings = get_settings()
                credentials_path = settings.GOOGLE_SHEETS_CREDENTIALS_PATH
            except Exception:
                # Fallback to environment variable if settings not available
                credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
            
            if not credentials_path:
                logger.warning("⚠️ GOOGLE_SHEETS_CREDENTIALS_PATH not set. Google Sheets integration disabled.")
                return
            
            if not os.path.exists(credentials_path):
                logger.warning(f"⚠️ Credentials file not found at: {credentials_path}")
                return
            
            # Create credentials
            creds = Credentials.from_service_account_file(
                credentials_path,
                scopes=scopes
            )
            
            # Initialize the client
            self.client = gspread.authorize(creds)
            logger.info("✅ Google Sheets client initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing Google Sheets client: {e}")
            self.client = None
    
    def is_initialized(self) -> bool:
        """Check if Google Sheets client is initialized"""
        return self.client is not None
    
    def append_questionnaire_result(
        self,
        user_email: str,
        questionnaire_data: Dict[str, Any],
        ml_predictions: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Append questionnaire result to Google Sheets
        
        Args:
            user_email: User's email
            questionnaire_data: Questionnaire answers
            ml_predictions: ML model predictions (optional)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_initialized() or self.client is None:
            logger.warning("Google Sheets client not initialized. Skipping write.")
            return False
        
        try:
            # Open the spreadsheet
            spreadsheet: Spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            worksheet: Worksheet = spreadsheet.worksheet(self.worksheet_name)
            
            # Prepare row data matching the CSV format
            row_data = self._prepare_row_data(user_email, questionnaire_data, ml_predictions)
            
            # Append the row
            worksheet.append_row(row_data, value_input_option=ValueInputOption.user_entered)
            
            logger.info(f"✅ Successfully appended questionnaire result for {user_email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error appending to Google Sheets: {e}")
            return False
    
    def _prepare_row_data(
        self,
        user_email: str,
        questionnaire_data: Dict[str, Any],
        ml_predictions: Optional[Dict[str, Any]] = None
    ) -> List[Any]:
        """
        Prepare row data in the same format as the CSV
        
        CSV columns:
        Timestamp, Academic Level, Primary Sport, Participation Years, Participation Level,
        Fitness Level, Technical Skill, Leadership, Data Comfort, Motivation,
        Career Importance, Work Environment, Biggest Challenge, Injury History,
        Career Interests (3), Education Level
        
        Additional columns for ML predictions:
        Top Career Prediction, Prediction Confidence, User Email
        """
        answers = questionnaire_data
        
        # Get timestamp
        timestamp = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        
        # Map questionnaire answers to row format
        row = [
            timestamp,
            self._to_sheet_cell(answers.get('academic_level', '')),
            self._to_sheet_cell(answers.get('primary_sport', '')),
            self._to_sheet_cell(answers.get('participation_years', '')),
            self._to_sheet_cell(answers.get('participation_level', '')),
            self._to_sheet_cell(answers.get('fitness_level', '')),
            self._to_sheet_cell(answers.get('technical_skill', '')),
            self._to_sheet_cell(answers.get('leadership', '')),
            self._to_sheet_cell(answers.get('data_comfort', '')),
            self._to_sheet_cell(answers.get('motivation', '')),
            self._to_sheet_cell(answers.get('career_importance', '')),
            self._to_sheet_cell(answers.get('work_environment', '')),
            self._to_sheet_cell(answers.get('biggest_challenge', '')),
            self._to_sheet_cell(answers.get('injury_history', '')),
            self._to_sheet_cell(answers.get('career_interests', '')),
            self._to_sheet_cell(answers.get('education_level', ''))
        ]
        
        # Add ML prediction columns if available
        if ml_predictions:
            row.extend([
                self._to_sheet_cell(ml_predictions.get('primary_prediction', '')),
                self._to_sheet_cell(ml_predictions.get('confidence', '')),
                self._to_sheet_cell(user_email)
            ])
        else:
            row.extend(['', '', self._to_sheet_cell(user_email)])
        
        return row

    def _to_sheet_cell(self, value: Any) -> Any:
        """Convert complex objects to scalar values accepted by Google Sheets."""
        if value is None:
            return ''

        if isinstance(value, (str, int, float, bool)):
            return value

        if isinstance(value, list):
            return ' | '.join(str(v) for v in value)

        if isinstance(value, dict):
            return json.dumps(value, ensure_ascii=True)

        return str(value)
    
    def get_all_responses(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get all responses from the spreadsheet
        
        Returns:
            List of dictionaries containing all responses
        """
        if not self.is_initialized() or self.client is None:
            logger.warning("Google Sheets client not initialized.")
            return None
        
        try:
            spreadsheet: Spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            worksheet: Worksheet = spreadsheet.worksheet(self.worksheet_name)
            
            # Get all records as dictionaries
            records = worksheet.get_all_records()
            logger.info(f"✅ Retrieved {len(records)} records from Google Sheets")
            return records
            
        except Exception as e:
            logger.error(f"❌ Error reading from Google Sheets: {e}")
            return None
    
    def update_spreadsheet_headers(self):
        """
        Update spreadsheet headers to include ML prediction columns
        This should be run once to set up the headers
        """
        if not self.is_initialized() or self.client is None:
            logger.warning("Google Sheets client not initialized.")
            return False
        
        try:
            spreadsheet: Spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            worksheet: Worksheet = spreadsheet.worksheet(self.worksheet_name)
            
            # Get current headers
            headers = worksheet.row_values(1)
            
            # Add new headers if they don't exist
            new_headers = ['Top Career Prediction', 'Prediction Confidence', 'User Email']
            
            for header in new_headers:
                if header not in headers:
                    headers.append(header)
            
            # Update the header row (range_name, values)
            worksheet.update(values=[headers], range_name='1:1')
            
            logger.info("✅ Spreadsheet headers updated successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error updating headers: {e}")
            return False


# Singleton instance
_sheets_service: Optional[GoogleSheetsService] = None


def get_sheets_service() -> GoogleSheetsService:
    """Get or create GoogleSheetsService singleton"""
    global _sheets_service
    if _sheets_service is None:
        _sheets_service = GoogleSheetsService()
    return _sheets_service
