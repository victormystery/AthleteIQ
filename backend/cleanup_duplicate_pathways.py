"""
Database cleanup script - Remove old duplicate pathways
Removes pathways with old slugs that have been replaced by new standardized ones
"""

import sys
import os
from pathlib import Path

# Add backend directory to path for imports
backend_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(backend_dir))

# Set working directory to backend
os.chdir(backend_dir)

from app.database.session import SessionLocal
from app.database.models import CareerPathway
from sqlalchemy import select

def cleanup_duplicate_pathways():
    """Remove old duplicate pathways with outdated slugs"""
    
    db = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("🧹 CLEANING UP DUPLICATE PATHWAYS")
        print("="*60)
        
        # Show all pathways before cleanup
        stmt = select(CareerPathway)
        all_pathways = db.execute(stmt).scalars().all()
        print(f"\n📊 Current pathways in database: {len(all_pathways)}\n")
        
        # Old pathways to remove (replaced by new standardized slugs)
        old_slugs_to_remove = [
            'coaching-development',  # Replaced by 'coaching'
            'high-performance-sport',  # Replaced by 'professional-athlete'
            'sports-science-medicine',  # Replaced by 'sports-science'
        ]
        
        print("🗑️  Pathways to remove:")
        for slug in old_slugs_to_remove:
            print(f"   - {slug}")
        print()
        
        # Delete old pathways
        deleted_count = 0
        for slug in old_slugs_to_remove:
            stmt = select(CareerPathway).where(CareerPathway.slug == slug)
            pathway = db.execute(stmt).scalar_one_or_none()
            
            if pathway:
                print(f"🗑️  Deleting: {pathway.title} (slug: {pathway.slug})")
                db.delete(pathway)
                deleted_count += 1
            else:
                print(f"⚠️  Not found: {slug}")
        
        # Commit deletions
        db.commit()
        print(f"\n✅ Deleted {deleted_count} old pathways")
        
        # Show remaining pathways
        stmt = select(CareerPathway)
        remaining_pathways = db.execute(stmt).scalars().all()
        
        print(f"\n📊 Total pathways after cleanup: {len(remaining_pathways)}")
        print("\n✅ Remaining pathways:")
        for i, pathway in enumerate(remaining_pathways, 1):
            salary_min = f"£{pathway.salary_range_min:,.0f}" if pathway.salary_range_min else "N/A"
            salary_max = f"£{pathway.salary_range_max:,.0f}" if pathway.salary_range_max else "N/A"
            skills_count = len(pathway.key_skills) if pathway.key_skills else 0
            
            print(f"  {i:2d}. {pathway.slug}")
            print(f"      Title: {pathway.title}")
            print(f"      Salary: {salary_min} - {salary_max}")
            print(f"      Skills: {skills_count} key skills")
            print()
        
        print("="*60)
        print("✅ CLEANUP SUCCESSFUL")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during cleanup: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_duplicate_pathways()
