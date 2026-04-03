"""
Seed Admin User Script
Creates a pre-seeded admin user in the database
"""
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database.session import SessionLocal, get_engine
from app.database.models import User, Profile, UserRole
from app.database.base import Base
from app.utils.auth import get_password_hash
import uuid


def generate_uuid():
    """Generate UUID for primary keys"""
    return str(uuid.uuid4())


def seed_admin_user(db: Session):
    """
    Create admin user if not exists
    
    Admin Details:
    - Name: Victor Admin
    - Email: oasrobovictors@gmail.com
    - Password: 12345678Dj@
    - Role: admin
    """
    admin_email = "oasrobovictors@gmail.com"
    
    # Check if admin already exists
    existing_admin = db.query(User).filter(User.email == admin_email).first()
    
    if existing_admin:
        print(f"✓ Admin user already exists: {admin_email}")
        print(f"  - User ID: {existing_admin.id}")
        print(f"  - Role: {existing_admin.role}")
        return existing_admin
    
    # Create admin user
    admin_id = generate_uuid()
    hashed_password = get_password_hash("12345678Dj@")
    
    admin_user = User(
        id=admin_id,
        email=admin_email,
        full_name="Victor Admin",
        hashed_password=hashed_password,
        role=UserRole.ADMIN,
        is_active=True,
    )
    
    db.add(admin_user)
    db.flush()  # Flush to get the user ID
    
    # Create admin profile
    admin_profile = Profile(
        id=generate_uuid(),
        user_id=admin_id,
        full_name="Victor Admin",
        avatar_url=None,
        university="System Administrator",
        programme_of_study="Administration",
        year_of_study=None,
        primary_sport=None,
        phone_number=None,
    )
    
    db.add(admin_profile)
    db.commit()
    
    print("✓ Admin user created successfully!")
    print(f"  - Email: {admin_email}")
    print(f"  - Password: 12345678Dj@")
    print(f"  - Role: admin")
    print(f"  - User ID: {admin_id}")
    
    return admin_user


def main():
    """Main function to seed admin user"""
    print("=" * 60)
    print("SEEDING ADMIN USER")
    print("=" * 60)
    
    # Get engine and create tables if they don't exist
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        seed_admin_user(db)
        print("\n" + "=" * 60)
        print("SEEDING COMPLETE")
        print("=" * 60)
    except Exception as e:
        print(f"\n✗ Error seeding admin user: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
