"""
Script to clean up duplicate questionnaire responses.
Keeps only the latest response for each user.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings
from app.database.models import QuestionnaireResponse
from app.database.base import Base

def cleanup_duplicate_questionnaires():
    """Remove duplicate questionnaire responses, keeping only the latest for each user"""
    
    # Create database connection
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        print("🔍 Checking for duplicate questionnaire responses...")
        
        # Get all users who have questionnaire responses
        all_responses = db.query(QuestionnaireResponse).order_by(
            QuestionnaireResponse.user_id,
            QuestionnaireResponse.created_at.desc()
        ).all()
        
        # Group by user_id
        user_responses = {}
        for response in all_responses:
            if response.user_id not in user_responses:
                user_responses[response.user_id] = []
            user_responses[response.user_id].append(response)
        
        # Find and delete duplicates
        total_deleted = 0
        users_with_duplicates = 0
        
        for user_id, responses in user_responses.items():
            if len(responses) > 1:
                users_with_duplicates += 1
                # Keep the first one (newest), delete the rest
                newest = responses[0]
                duplicates = responses[1:]
                
                print(f"\n👤 User {user_id}:")
                print(f"  - Has {len(responses)} responses")
                print(f"  - Keeping: {newest.id} (created: {newest.created_at})")
                
                for duplicate in duplicates:
                    print(f"  - Deleting: {duplicate.id} (created: {duplicate.created_at})")
                    db.delete(duplicate)
                    total_deleted += 1
        
        # Commit the changes
        if total_deleted > 0:
            db.commit()
            print(f"\n✅ Successfully deleted {total_deleted} duplicate responses from {users_with_duplicates} users")
        else:
            print("\n✅ No duplicate questionnaire responses found!")
        
    except Exception as e:
        print(f"\n❌ Error cleaning up duplicates: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_duplicate_questionnaires()
