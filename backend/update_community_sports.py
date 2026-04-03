"""
Update recreational-fitness pathway title to Community Sports
"""
import sys
import os
from pathlib import Path

# Add backend directory to path for imports
backend_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(backend_dir))
os.chdir(backend_dir)

from app.database.session import SessionLocal
from app.database.models import CareerPathway

def update_community_sports_title():
    """Update the title for recreational-fitness pathway"""
    
    db = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("✏️  UPDATING PATHWAY TITLE")
        print("="*60 + "\n")
        
        # Find the pathway
        pathway = db.query(CareerPathway).filter(
            CareerPathway.slug == 'recreational-fitness'
        ).first()
        
        if pathway:
            old_title = pathway.title
            pathway.title = "Community Sports"
            
            db.commit()
            
            print(f"✅ Updated pathway title:")
            print(f"   Slug: {pathway.slug}")
            print(f"   Old title: {old_title}")
            print(f"   New title: {pathway.title}")
            print(f"\n{'='*60}")
            print("✅ UPDATE SUCCESSFUL")
            print("="*60 + "\n")
        else:
            print("❌ Pathway not found: recreational-fitness\n")
            
    except Exception as e:
        print(f"\n❌ Error during update: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    update_community_sports_title()
