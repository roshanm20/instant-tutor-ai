#!/usr/bin/env python3
"""
Test script for Kerala AI Tutor API
"""

import requests
import json
import time

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        print("✅ Health Check:")
        print(json.dumps(response.json(), indent=2))
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_query():
    """Test query endpoint"""
    try:
        headers = {
            "Authorization": "Bearer demo-token-123",
            "Content-Type": "application/json"
        }
        
        data = {
            "query": "What is the derivative of x squared?",
            "course_id": "MATH_101",
            "user_id": "student_123"
        }
        
        response = requests.post("http://localhost:8000/api/query", 
                               headers=headers, 
                               json=data)
        
        print("\n✅ Query Test:")
        print(json.dumps(response.json(), indent=2))
        return True
    except Exception as e:
        print(f"❌ Query test failed: {e}")
        return False

def test_kerala_features():
    """Test Kerala-specific features"""
    try:
        response = requests.get("http://localhost:8000/api/kerala/features")
        print("\n✅ Kerala Features:")
        print(json.dumps(response.json(), indent=2))
        return True
    except Exception as e:
        print(f"❌ Kerala features test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Kerala AI Tutor API")
    print("=" * 50)
    
    # Wait a moment for server to start
    time.sleep(2)
    
    tests = [
        test_health,
        test_query,
        test_kerala_features
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! Kerala AI Tutor is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the server logs.")

if __name__ == "__main__":
    main()
