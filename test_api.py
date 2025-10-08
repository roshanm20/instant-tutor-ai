#!/usr/bin/env python3
"""
Simple API test script for Instant Tutor AI
Tests all endpoints to ensure everything is working
"""

import requests
import json
import time

def test_api():
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Instant Tutor AI API")
    print("=" * 50)
    
    # Test 1: Health Check
    print("1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health Check: PASSED")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health Check: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Health Check: ERROR - {e}")
    
    print()
    
    # Test 2: Kerala Features
    print("2. Testing Kerala Features...")
    try:
        response = requests.get(f"{base_url}/api/kerala/features", timeout=5)
        if response.status_code == 200:
            print("✅ Kerala Features: PASSED")
            data = response.json()
            print(f"   Languages: {data.get('language_support', 'N/A')}")
            print(f"   Curricula: {data.get('curriculum_alignment', 'N/A')}")
        else:
            print(f"❌ Kerala Features: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Kerala Features: ERROR - {e}")
    
    print()
    
    # Test 3: Query Endpoint
    print("3. Testing Query Endpoint...")
    try:
        headers = {"Authorization": "Bearer demo-token-123"}
        payload = {
            "query": "What is the derivative of x²?",
            "course_id": "MATH_101",
            "user_id": "test_user"
        }
        response = requests.post(f"{base_url}/api/query", 
                               json=payload, 
                               headers=headers, 
                               timeout=10)
        if response.status_code == 200:
            print("✅ Query Endpoint: PASSED")
            data = response.json()
            print(f"   Answer: {data.get('answer', 'N/A')[:100]}...")
            print(f"   Confidence: {data.get('confidence', 'N/A')}")
        else:
            print(f"❌ Query Endpoint: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Query Endpoint: ERROR - {e}")
    
    print()
    
    # Test 4: Course Upload
    print("4. Testing Course Upload...")
    try:
        headers = {"Authorization": "Bearer demo-token-123"}
        payload = {
            "course_id": "TEST_101",
            "course_title": "Test Course",
            "video_urls": ["test_video.mp4"],
            "language": "english",
            "difficulty": "beginner"
        }
        response = requests.post(f"{base_url}/api/courses/upload", 
                               json=payload, 
                               headers=headers, 
                               timeout=5)
        if response.status_code == 200:
            print("✅ Course Upload: PASSED")
            data = response.json()
            print(f"   Message: {data.get('message', 'N/A')}")
        else:
            print(f"❌ Course Upload: FAILED ({response.status_code})")
    except Exception as e:
        print(f"❌ Course Upload: ERROR - {e}")
    
    print()
    print("🎉 API Testing Complete!")
    print("=" * 50)

if __name__ == "__main__":
    test_api()
