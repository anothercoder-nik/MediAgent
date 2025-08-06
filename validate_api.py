"""
Quick validation script for the Flask API
"""
import requests
import json

def test_health():
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Could not connect to API: {e}")
        return False

def test_agents_import():
    try:
        from Utils.Agents import (
            extract_text_from_pdf, structure_medical_report,
            Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam,
            generate_report_pdf
        )
        print("✅ All agent imports successful")
        return True
    except Exception as e:
        print(f"❌ Agent import failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Validating Flask API and Agents compatibility\n")
    
    # Test 1: Agent imports
    print("1. Testing agent imports...")
    agents_ok = test_agents_import()
    print()
    
    # Test 2: API health
    print("2. Testing API health...")
    api_ok = test_health()
    print()
    
    if agents_ok and api_ok:
        print("🎉 All tests passed! Your Flask API is compatible with Agents.py")
    else:
        print("⚠️  Some issues found. Check the output above.")
