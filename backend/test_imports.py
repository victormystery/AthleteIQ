"""
Quick test to verify all imports work correctly
"""
print("Testing imports...")

# Test main imports
print("1. Testing main.py imports...")
try:
    from main import app, create_app
    print("   ✓ main.py imports successful")
except Exception as e:
    print(f"   ✗ main.py import error: {e}")

# Test database imports
print("2. Testing database imports...")
try:
    from app.database.session import engine, SessionLocal, get_db, init_db
    from app.database.base import Base
    from app.database.models import User, Profile, CareerPathway
    print("   ✓ Database imports successful")
except Exception as e:
    print(f"   ✗ Database import error: {e}")

# Test CRUD imports
print("3. Testing CRUD imports...")
try:
    from app.crud import (
        user_crud,
        profile_crud,
        pathway_crud,
        questionnaire_crud,
        recommendation_crud,
        feedback_crud,
        progress_crud
    )
    print("   ✓ CRUD imports successful")
except Exception as e:
    print(f"   ✗ CRUD import error: {e}")

# Test route imports
print("4. Testing route imports...")
try:
    from app.routes.auth_routes import router as auth_router
    from app.routes.profile_routes import router as profile_router
    from app.routes.career_routes_v2 import router as career_router_v2
    from app.routes.questionnaire_routes import router as questionnaire_router
    from app.routes.feedback_routes import router as feedback_router
    from app.routes.progress_routes import router as progress_router
    print("   ✓ Route imports successful")
except Exception as e:
    print(f"   ✗ Route import error: {e}")

# Test controller imports
print("5. Testing controller imports...")
try:
    from app.controllers.auth_controller import auth_controller
    from app.controllers.profile_controller import profile_controller
    from app.controllers.career_controller_v2 import career_controller_v2
    print("   ✓ Controller imports successful")
except Exception as e:
    print(f"   ✗ Controller import error: {e}")

# Test service imports
print("6. Testing service imports...")
try:
    from app.services.ml_service import ml_service
    from app.services.career_analysis_service import career_analysis_service
    from app.services.database_service import init_database_data
    print("   ✓ Service imports successful")
except Exception as e:
    print(f"   ✗ Service import error: {e}")

# Test utils imports
print("7. Testing utils imports...")
try:
    from app.utils.auth import create_access_token, verify_token, get_current_user
    from app.utils.logger import setup_logging
    from app.utils.exceptions import register_exception_handlers
    print("   ✓ Utils imports successful")
except Exception as e:
    print(f"   ✗ Utils import error: {e}")

print("\n" + "="*60)
print("All import tests completed!")
print("="*60)
print("\nYou can now start the server with:")
print("  uvicorn main:app --reload")
