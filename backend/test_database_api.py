"""
Test Database Setup and API Endpoints
Run this script to verify the database integration is working correctly
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def test_health_check():
    print_section("1. Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_register():
    print_section("2. User Registration")
    try:
        data = {
            "email": f"test.user.{datetime.now().timestamp()}@example.com",
            "password": "TestPass123!",
            "full_name": "Test User",
            "university": "Sports University",
            "year_of_study": 2,
            "primary_sport": "Football"
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        print(f"Status: {response.status_code}")
        result = response.json()
        print(json.dumps(result, indent=2))
        return result.get("access_token")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_login(email="test@example.com", password="TestPass123!"):
    print_section("3. User Login")
    try:
        data = {
            "username": email,
            "password": password
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Token: {result.get('access_token', 'N/A')[:50]}...")
        return result.get("access_token")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_get_current_user(token):
    print_section("4. Get Current User Info")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_get_pathways():
    print_section("5. Get Career Pathways")
    try:
        response = requests.get(f"{BASE_URL}/api/career/pathways")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Total Pathways: {result.get('total_pathways', 0)}")
        if result.get('pathways'):
            print("\nPathways:")
            for pathway in result['pathways']:
                print(f"  - {pathway['title']} ({pathway['slug']})")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_get_recommendations(token=None):
    print_section("6. Get Career Recommendations")
    try:
        questionnaire_data = {
            "academic_level": "Undergraduate",
            "primary_sport": "Football",
            "participation_years": 8,
            "participation_level": "University",
            "fitness_level": 8,
            "technical_skill": 7,
            "leadership": 6,
            "motivation": "Helping others",
            "career_interests": "Coaching",
            "academic_performance": "Good",
            "communication": 8,
            "organization": 7,
            "available_hours": "10-20 hours",
            "prefer_environment": "Indoor"
        }
        
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
            print("🔐 Authenticated request (will save to database)")
        else:
            print("👤 Anonymous request (won't save to database)")
        
        response = requests.post(
            f"{BASE_URL}/api/career/predict",
            json=questionnaire_data,
            headers=headers
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"\nPrimary Prediction: {result.get('primary_prediction')}")
        print(f"Total Recommendations: {len(result.get('all_recommendations', []))}")
        if result.get('all_recommendations'):
            print("\nTop 3 Recommendations:")
            for i, rec in enumerate(result['all_recommendations'][:3], 1):
                print(f"  {i}. {rec['career']} (Match: {rec.get('match_score', 0):.0%})")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_get_my_recommendations(token):
    print_section("7. Get Saved Recommendations")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BASE_URL}/api/career/recommendations",
            headers=headers
        )
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Total Saved: {result.get('total', 0)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_profile_operations(token):
    print_section("8. Profile Operations")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        
        # Get profile
        print("Getting profile...")
        response = requests.get(f"{BASE_URL}/api/profile", headers=headers)
        print(f"Get Status: {response.status_code}")
        profile = response.json()
        print(f"Current Sport: {profile.get('primary_sport')}")
        
        # Update profile
        print("\nUpdating profile...")
        update_data = {
            "year_of_study": 3,
            "primary_sport": "Basketball"
        }
        response = requests.put(
            f"{BASE_URL}/api/profile",
            json=update_data,
            headers=headers
        )
        print(f"Update Status: {response.status_code}")
        updated = response.json()
        print(f"Updated Sport: {updated.get('primary_sport')}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def run_all_tests():
    print("\n" + "🚀 "*30)
    print("CAREER RECOMMENDER API - DATABASE INTEGRATION TEST")
    print("🚀 "*30)
    
    results = []
    
    # Test 1: Health check
    results.append(("Health Check", test_health_check()))
    
    # Test 2: Register new user
    token = test_register()
    results.append(("Registration", token is not None))
    
    if not token:
        print("\n⚠️  Registration failed, attempting login with test credentials")
        token = test_login()
    
    if token:
        # Test 3: Get current user
        results.append(("Get User Info", test_get_current_user(token)))
        
        # Test 4: Get pathways
        results.append(("Get Pathways", test_get_pathways()))
        
        # Test 5: Get recommendations (authenticated)
        results.append(("Get Recommendations (Auth)", test_get_recommendations(token)))
        
        # Test 6: Get saved recommendations
        results.append(("Get Saved Recommendations", test_get_my_recommendations(token)))
        
        # Test 7: Profile operations
        results.append(("Profile Operations", test_profile_operations(token)))
    else:
        print("\n❌ No authentication token available. Skipping authenticated tests.")
        results.extend([
            ("Get User Info", False),
            ("Get Pathways", test_get_pathways()),
            ("Get Recommendations (Auth)", False),
            ("Get Saved Recommendations", False),
            ("Profile Operations", False)
        ])
    
    # Test 8: Anonymous recommendations
    print_section("9. Anonymous Recommendations")
    results.append(("Anonymous Recommendations", test_get_recommendations(None)))
    
    # Print summary
    print_section("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{'='*60}")
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print(f"{'='*60}\n")
    
    if passed == total:
        print("🎉 All tests passed! Database integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        print("💡 Make sure the server is running: uvicorn main:app --reload")

if __name__ == "__main__":
    print("\n⚠️  Make sure the server is running on http://localhost:8000")
    input("Press Enter to start tests...")
    run_all_tests()
