"""
Script to seed/reseed the database with career pathway data
"""
import sys
import logging
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from app.database.session import SessionLocal
from app.services.database_service import seed_career_pathways
from app.crud.pathway import pathway_crud

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """
    Seed the database with all 10 career pathways
    """
    print("=" * 60)
    print("CAREER PATHWAYS DATABASE SEEDING")
    print("=" * 60)
    
    db = SessionLocal()
    
    try:
        # Check existing pathways
        existing_pathways = pathway_crud.get_multi(db, limit=100)
        print(f"\n📊 Current pathways in database: {len(existing_pathways)}")
        
        if existing_pathways:
            print("\nExisting pathways:")
            for pathway in existing_pathways:
                print(f"  - {pathway.slug}: {pathway.title}")
        
        # Seed pathways
        print("\n" + "=" * 60)
        print("SEEDING PATHWAYS...")
        print("=" * 60)
        
        pathways = seed_career_pathways(db)
        
        print("\n" + "=" * 60)
        print(f"✅ COMPLETED: {len(pathways)} pathways in database")
        print("=" * 60)
        
        # Show all pathways
        all_pathways = pathway_crud.get_multi(db, limit=100)
        print(f"\n📊 Total pathways now in database: {len(all_pathways)}")
        print("\nAll pathways:")
        for i, pathway in enumerate(all_pathways, 1):
            print(f"  {i}. {pathway.slug}: {pathway.title}")
            print(f"     Salary: £{pathway.salary_range_min:,} - £{pathway.salary_range_max:,}")
            # Get key_skills safely
            key_skills = getattr(pathway, 'key_skills', None)
            skills_count = len(key_skills) if key_skills and isinstance(key_skills, list) else 0
            print(f"     Skills: {skills_count} key skills")
        
        print("\n" + "=" * 60)
        print("✅ DATABASE SEEDING SUCCESSFUL")
        print("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Error seeding database: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
