#!/usr/bin/env python3
"""
Debug API request to understand the 422 error
"""

import requests
import json

def debug_api_request():
    """Debug the API request to understand the 422 error"""
    print("🔍 Debugging API Request - 422 Error")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test the exact request the frontend is making
    print("1. Testing exact frontend request...")
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer demo-token-123"
        }
        payload = {
            "query": "What is calculus?",
            "course_id": "MATH_101",
            "user_id": "student_123"
        }
        
        print(f"   Headers: {headers}")
        print(f"   Payload: {payload}")
        
        response = requests.post(f"{base_url}/api/query", 
                               json=payload, 
                               headers=headers, 
                               timeout=5)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Request successful!")
            data = response.json()
            print(f"   Answer: {data.get('answer', 'N/A')[:100]}...")
        else:
            print(f"❌ Request failed with status {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error details: {error_data}")
            except:
                print(f"   Error text: {response.text}")
                
    except Exception as e:
        print(f"❌ Request error: {e}")
    
    # Test with minimal request
    print("\n2. Testing minimal request...")
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer demo-token-123"
        }
        payload = {
            "query": "Test",
            "course_id": "TEST"
        }
        
        response = requests.post(f"{base_url}/api/query", 
                               json=payload, 
                               headers=headers, 
                               timeout=5)
        
        print(f"   Status Code: {response.status_code}")
        if response.status_code != 200:
            try:
                error_data = response.json()
                print(f"   Error details: {error_data}")
            except:
                print(f"   Error text: {response.text}")
        else:
            print("✅ Minimal request successful!")
            
    except Exception as e:
        print(f"❌ Minimal request error: {e}")
    
    # Test with different field names
    print("\n3. Testing with different field names...")
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer demo-token-123"
        }
        payload = {
            "query": "What is math?",
            "course_id": "MATH_101",
            "user_id": "test_user"
        }
        
        response = requests.post(f"{base_url}/api/query", 
                               json=payload, 
                               headers=headers, 
                               timeout=5)
        
        print(f"   Status Code: {response.status_code}")
        if response.status_code != 200:
            try:
                error_data = response.json()
                print(f"   Error details: {error_data}")
            except:
                print(f"   Error text: {response.text}")
        else:
            print("✅ Different field names successful!")
            
    except Exception as e:
        print(f"❌ Different field names error: {e}")

if __name__ == "__main__":
    debug_api_request()
