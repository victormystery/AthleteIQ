#!/usr/bin/env python
"""
Quick Setup Script for ML & Google Sheets Integration
Helps verify the setup is correct
"""
import os
import sys

# Add the backend directory to the path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)


def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  ❌ Python {version.major}.{version.minor} (need 3.8+)")
        return False


def check_dependencies():
    """Check if required packages are installed"""
    print("\nChecking dependencies...")
    required = ['gspread', 'google.auth', 'joblib', 'pandas', 'numpy', 'sklearn', 'fastapi']
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (not installed)")
            missing.append(package)
    
    if missing:
        print(f"\n  Install missing packages with:")
        print(f"  pip install -r requirements.txt")
        return False
    return True


def check_model_file():
    """Check if ML model file exists"""
    print("\nChecking ML model...")
    model_path = os.path.join(backend_dir, "sports_career_recommendation_model.pkl")
    
    if os.path.exists(model_path):
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"  ✅ Model found ({size_mb:.2f} MB)")
        return True
    else:
        print(f"  ❌ Model not found at: {model_path}")
        print(f"  Run the Jupyter notebook to train and save the model:")
        print(f"  student-football-analysis/notebooks/student_sports_career_analysis_v2.ipynb")
        return False


def check_training_data():
    """Check if training data CSV exists"""
    print("\nChecking training data...")
    
    # Go up from backend to project root
    project_root = os.path.dirname(backend_dir)
    csv_path = os.path.join(
        project_root,
        "student-football-analysis",
        "data",
        "Student Sports Career Pathway Questionnaire (Responses) - Form Responses 1.csv"
    )
    
    if os.path.exists(csv_path):
        # Try to read the CSV to check it's valid
        try:
            import pandas as pd
            df = pd.read_csv(csv_path)
            print(f"  ✅ Training data found ({len(df)} responses)")
            return True
        except Exception as e:
            print(f"  ❌ Training data exists but can't be read: {e}")
            return False
    else:
        print(f"  ❌ Training data not found at: {csv_path}")
        return False


def check_google_sheets_config():
    """Check Google Sheets configuration"""
    print("\nChecking Google Sheets configuration...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    creds_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
    
    if not creds_path:
        print(f"  ⚠️  GOOGLE_SHEETS_CREDENTIALS_PATH not set in .env")
        print(f"  Google Sheets integration will be disabled")
        print(f"  See GOOGLE_SHEETS_SETUP.md for setup instructions")
        return None  # Not an error, just optional
    
    if not os.path.exists(creds_path):
        print(f"  ❌ Credentials file not found at: {creds_path}")
        return False
    
    # Try to load the credentials
    try:
        import json
        with open(creds_path, 'r') as f:
            creds_data = json.load(f)
        
        if 'client_email' in creds_data:
            print(f"  ✅ Credentials valid")
            print(f"     Service account: {creds_data['client_email']}")
            return True
        else:
            print(f"  ❌ Credentials file is not a valid service account JSON")
            return False
    except Exception as e:
        print(f"  ❌ Error reading credentials: {e}")
        return False


def test_ml_service():
    """Test if ML service can load the model"""
    print("\nTesting ML service...")
    
    try:
        from app.services.ml_service import ml_service
        
        if ml_service.is_model_loaded():
            print(f"  ✅ ML service initialized")
            if ml_service.classes is not None:
                print(f"     Career pathways: {len(ml_service.classes)}")
            return True
        else:
            print(f"  ❌ ML service failed to load model")
            return False
    except Exception as e:
        print(f"  ❌ Error loading ML service: {e}")
        return False


def test_google_sheets_service():
    """Test if Google Sheets service can initialize"""
    print("\nTesting Google Sheets service...")
    
    try:
        from app.services.google_sheets_service import get_sheets_service
        
        sheets_service = get_sheets_service()
        
        if sheets_service.is_initialized():
            print(f"  ✅ Google Sheets service initialized")
            print(f"     Spreadsheet ID: {sheets_service.spreadsheet_id}")
            return True
        else:
            print(f"  ⚠️  Google Sheets service not initialized (optional)")
            return None  # Not an error
    except Exception as e:
        print(f"  ❌ Error initializing Google Sheets service: {e}")
        return False


def main():
    """Run all checks"""
    print("=" * 80)
    print("ML & Google Sheets Integration Setup Checker")
    print("=" * 80)
    print()
    
    checks = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'ML Model': check_model_file(),
        'Training Data': check_training_data(),
        'Google Sheets Config': check_google_sheets_config(),
        'ML Service': test_ml_service(),
        'Google Sheets Service': test_google_sheets_service(),
    }
    
    print()
    print("=" * 80)
    print("Setup Summary")
    print("=" * 80)
    
    required_passed = 0
    required_total = 0
    optional_passed = 0
    
    for check_name, result in checks.items():
        if check_name in ['Google Sheets Config', 'Google Sheets Service']:
            # Optional checks
            if result is True:
                optional_passed += 1
                print(f"  ✅ {check_name}")
            elif result is None:
                print(f"  ⚠️  {check_name} (optional - not configured)")
            else:
                print(f"  ❌ {check_name} (optional)")
        else:
            # Required checks
            required_total += 1
            if result is True:
                required_passed += 1
                print(f"  ✅ {check_name}")
            else:
                print(f"  ❌ {check_name}")
    
    print()
    print(f"Required checks: {required_passed}/{required_total} passed")
    print(f"Optional checks: {optional_passed}/2 configured")
    print()
    
    if required_passed == required_total:
        print("🎉 Setup complete! You can start the backend server.")
        print()
        print("Next steps:")
        print("  1. python main.py  (start the backend)")
        print("  2. Submit a questionnaire through the API")
        print("  3. Check that predictions are generated")
        if optional_passed == 0:
            print()
            print("Optional: Set up Google Sheets integration")
            print("  See GOOGLE_SHEETS_SETUP.md for instructions")
        return 0
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
        print()
        print("For help, see:")
        print("  • ML_INTEGRATION_GUIDE.md - Quick reference")
        print("  • GOOGLE_SHEETS_SETUP.md - Google Sheets setup")
        return 1


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
