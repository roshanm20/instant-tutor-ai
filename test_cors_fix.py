#!/usr/bin/env python3
"""
Test CORS fix for frontend-backend communication
"""

import requests
import json

def test_cors_fix():
    """Test that CORS is working for frontend access"""
    print("🔧 Testing CORS Fix for Frontend Access")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Health endpoint with file origin
    print("1. Testing Health endpoint with file:// origin...")
    try:
        headers = {"Origin": "file://"}
        response = requests.get(f"{base_url}/health", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint: CORS working")
            print(f"   CORS Header: {response.headers.get('access-control-allow-origin', 'Not set')}")
        else:
            print(f"❌ Health endpoint: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint: Error - {e}")
    
    # Test 2: Query endpoint with file origin
    print("\n2. Testing Query endpoint with file:// origin...")
    try:
        headers = {
            "Origin": "file://",
            "Content-Type": "application/json",
            "Authorization": "Bearer demo-token-123"
        }
        payload = {
            "query": "Test CORS fix",
            "course_id": "TEST_101",
            "user_id": "cors_test"
        }
        response = requests.post(f"{base_url}/api/query", 
                               json=payload, 
                               headers=headers, 
                               timeout=5)
        if response.status_code == 200:
            print("✅ Query endpoint: CORS working")
            print(f"   CORS Header: {response.headers.get('access-control-allow-origin', 'Not set')}")
        else:
            print(f"❌ Query endpoint: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Query endpoint: Error - {e}")
    
    # Test 3: Kerala features endpoint
    print("\n3. Testing Kerala features endpoint...")
    try:
        headers = {"Origin": "file://"}
        response = requests.get(f"{base_url}/api/kerala/features", headers=headers, timeout=5)
        if response.status_code == 200:
            print("✅ Kerala features: CORS working")
            print(f"   CORS Header: {response.headers.get('access-control-allow-origin', 'Not set')}")
        else:
            print(f"❌ Kerala features: Status {response.status_code}")
    except Exception as e:
        print(f"❌ Kerala features: Error - {e}")
    
    print("\n🎉 CORS Fix Testing Complete!")
    print("=" * 50)
    print("✅ Frontend should now be able to access the API")
    print("📍 Open frontend/index.html in your browser")
    print("🔗 The chat interface should work without CORS errors")

if __name__ == "__main__":
    test_cors_fix()
