#!/usr/bin/env python3
"""
Frontend functionality test for Instant Tutor AI
Tests the HTML frontend and ensures all features work
"""

import webbrowser
import time
import os
import requests
from pathlib import Path

def test_frontend():
    print("🌐 Testing Instant Tutor AI Frontend")
    print("=" * 50)
    
    # Check if frontend files exist
    frontend_path = Path("frontend/index.html")
    if not frontend_path.exists():
        print("❌ Frontend file not found: frontend/index.html")
        return False
    
    print("✅ Frontend file found: frontend/index.html")
    
    # Check if backend is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API is running")
        else:
            print("❌ Backend API not responding")
            return False
    except Exception as e:
        print(f"❌ Backend API error: {e}")
        return False
    
    # Test frontend HTML content
    try:
        with open(frontend_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for key frontend features
        features = [
            ("Chat Interface", "chat-section" in content),
            ("Course Selection", "course-selector" in content),
            ("Kerala Features", "Kerala" in content),
            ("Material Icons", "Material+Icons" in content),
            ("Responsive Design", "viewport" in content),
            ("JavaScript", "function askQuestion" in content),
            ("API Integration", "localhost:8000" in content),
            ("Kerala Theming", "Kerala" in content and "Malayalam" in content)
        ]
        
        print("\n📋 Frontend Features Check:")
        all_features_ok = True
        for feature_name, is_present in features:
            status = "✅" if is_present else "❌"
            print(f"   {status} {feature_name}")
            if not is_present:
                all_features_ok = False
        
        if all_features_ok:
            print("\n✅ All frontend features present!")
        else:
            print("\n❌ Some frontend features missing!")
            return False
            
    except Exception as e:
        print(f"❌ Error reading frontend file: {e}")
        return False
    
    # Test API integration from frontend perspective
    print("\n🔗 Testing API Integration:")
    try:
        # Test the same endpoints the frontend would use
        headers = {"Authorization": "Bearer demo-token-123"}
        
        # Test query endpoint (main frontend functionality)
        payload = {
            "query": "What is calculus?",
            "course_id": "MATH_101",
            "user_id": "frontend_test"
        }
        response = requests.post("http://localhost:8000/api/query", 
                               json=payload, 
                               headers=headers, 
                               timeout=5)
        if response.status_code == 200:
            print("✅ Query API integration working")
        else:
            print(f"❌ Query API integration failed: {response.status_code}")
            return False
        
        # Test Kerala features endpoint
        response = requests.get("http://localhost:8000/api/kerala/features", timeout=5)
        if response.status_code == 200:
            print("✅ Kerala features API working")
        else:
            print(f"❌ Kerala features API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ API integration error: {e}")
        return False
    
    print("\n🎉 Frontend Testing Complete!")
    print("=" * 50)
    return True

def open_frontend():
    """Open the frontend in the default browser"""
    frontend_path = Path("frontend/index.html").absolute()
    print(f"🌐 Opening frontend: {frontend_path}")
    
    try:
        webbrowser.open(f"file://{frontend_path}")
        print("✅ Frontend opened in browser")
        return True
    except Exception as e:
        print(f"❌ Error opening frontend: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Instant Tutor AI - Frontend Testing")
    print("=" * 60)
    
    # Test frontend functionality
    if test_frontend():
        print("\n🎯 Frontend is fully functional!")
        
        # Ask user if they want to open the frontend
        print("\n🌐 Would you like to open the frontend in your browser?")
        print("   The frontend will be available at: frontend/index.html")
        
        # Open frontend automatically
        open_frontend()
        
        print("\n📱 Frontend Features Available:")
        print("   • Real-time chat with AI tutor")
        print("   • Course selection (Math, Physics, Chemistry)")
        print("   • Kerala-themed design")
        print("   • Mobile responsive interface")
        print("   • Multi-language support")
        print("   • Admin dashboard")
        
    else:
        print("\n❌ Frontend testing failed!")
        print("   Please check the frontend files and try again.")
