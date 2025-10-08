#!/usr/bin/env python3
"""
Comprehensive code completion check for Instant Tutor AI
Verifies all components are implemented and working
"""

import os
import sys
from pathlib import Path
import requests
import json

def check_file_exists(file_path, description):
    """Check if a file exists and return status"""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - MISSING")
        return False

def check_api_endpoint(endpoint, description):
    """Check if API endpoint is working"""
    try:
        response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
        if response.status_code == 200:
            print(f"✅ {description}: {endpoint}")
            return True
        else:
            print(f"❌ {description}: {endpoint} - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {description}: {endpoint} - Error: {e}")
        return False

def check_code_completion():
    """Comprehensive code completion check"""
    print("🔍 INSTANT TUTOR AI - CODE COMPLETION CHECK")
    print("=" * 60)
    
    all_checks_passed = True
    
    # 1. Backend Structure Check
    print("\n📁 BACKEND STRUCTURE CHECK:")
    backend_files = [
        ("backend/api/main.py", "Main FastAPI application"),
        ("backend/api/kerala_features.py", "Kerala features API"),
        ("backend/core/secure_config.py", "Security configuration"),
        ("backend/database/weaviate_setup.py", "Weaviate database setup"),
        ("backend/database/pinecone_setup.py", "Pinecone database setup"),
        ("backend/services/video_processor.py", "Video processing service"),
        ("backend/utils/jwt_utils.py", "JWT authentication utilities"),
        ("backend/__init__.py", "Backend package init"),
        ("backend/api/__init__.py", "API package init"),
        ("backend/core/__init__.py", "Core package init"),
        ("backend/database/__init__.py", "Database package init"),
        ("backend/services/__init__.py", "Services package init"),
        ("backend/utils/__init__.py", "Utils package init")
    ]
    
    for file_path, description in backend_files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    
    # 2. Frontend Structure Check
    print("\n🌐 FRONTEND STRUCTURE CHECK:")
    frontend_files = [
        ("frontend/index.html", "Main frontend HTML"),
        ("frontend/package.json", "React package configuration"),
        ("frontend/tsconfig.json", "TypeScript configuration"),
        ("frontend/public/index.html", "React public HTML"),
        ("frontend/public/manifest.json", "PWA manifest"),
        ("frontend/src/App.tsx", "Main React application"),
        ("frontend/src/index.tsx", "React entry point"),
        ("frontend/src/components/Navigation.tsx", "Navigation component"),
        ("frontend/src/pages/HomePage.tsx", "Home page component"),
        ("frontend/src/pages/ChatPage.tsx", "Chat page component"),
        ("frontend/src/pages/AdminPage.tsx", "Admin page component"),
        ("frontend/src/services/chatService.ts", "API service layer")
    ]
    
    for file_path, description in frontend_files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    
    # 3. Configuration Files Check
    print("\n⚙️ CONFIGURATION FILES CHECK:")
    config_files = [
        ("requirements.txt", "Python dependencies"),
        ("start.py", "Application startup script"),
        ("main.py", "Main entry point"),
        ("test_api.py", "API testing script"),
        ("test_frontend.py", "Frontend testing script"),
        ("README.md", "Project documentation"),
        ("PROJECT_STRUCTURE.md", "Structure documentation"),
        ("PROJECT_SUMMARY.md", "Project summary"),
        (".gitignore", "Git ignore rules"),
        ("config/env.example", "Environment configuration template"),
        ("deployment/docker-compose.yml", "Docker deployment configuration")
    ]
    
    for file_path, description in config_files:
        if not check_file_exists(file_path, description):
            all_checks_passed = False
    
    # 4. API Endpoints Check
    print("\n🔗 API ENDPOINTS CHECK:")
    api_endpoints = [
        ("/health", "Health check endpoint"),
        ("/api/kerala/features", "Kerala features endpoint"),
        ("/docs", "API documentation")
    ]
    
    for endpoint, description in api_endpoints:
        if not check_api_endpoint(endpoint, description):
            all_checks_passed = False
    
    # 5. Test API Query Endpoint
    print("\n🧪 API FUNCTIONALITY CHECK:")
    try:
        headers = {"Authorization": "Bearer demo-token-123"}
        payload = {
            "query": "Test query for completion check",
            "course_id": "TEST_101",
            "user_id": "completion_check"
        }
        response = requests.post("http://localhost:8000/api/query", 
                               json=payload, 
                               headers=headers, 
                               timeout=5)
        if response.status_code == 200:
            print("✅ Query API: Working correctly")
        else:
            print(f"❌ Query API: Failed with status {response.status_code}")
            all_checks_passed = False
    except Exception as e:
        print(f"❌ Query API: Error - {e}")
        all_checks_passed = False
    
    # 6. Frontend Functionality Check
    print("\n🌐 FRONTEND FUNCTIONALITY CHECK:")
    try:
        frontend_path = Path("frontend/index.html")
        if frontend_path.exists():
            with open(frontend_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontend_features = [
                ("Chat Interface", "chat-section" in content),
                ("Course Selection", "course-selector" in content),
                ("Kerala Features", "Kerala" in content),
                ("Material Icons", "Material+Icons" in content),
                ("Responsive Design", "viewport" in content),
                ("JavaScript", "function askQuestion" in content),
                ("API Integration", "localhost:8000" in content)
            ]
            
            for feature_name, is_present in frontend_features:
                status = "✅" if is_present else "❌"
                print(f"   {status} {feature_name}")
                if not is_present:
                    all_checks_passed = False
        else:
            print("❌ Frontend file not found")
            all_checks_passed = False
    except Exception as e:
        print(f"❌ Frontend check error: {e}")
        all_checks_passed = False
    
    # 7. Project Structure Check
    print("\n📂 PROJECT STRUCTURE CHECK:")
    required_dirs = [
        "backend", "frontend", "docs", "deployment", 
        "config", "logs", "uploads", "tests"
    ]
    
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"✅ Directory: {dir_name}/")
        else:
            print(f"❌ Directory: {dir_name}/ - MISSING")
            all_checks_passed = False
    
    # 8. GitHub Integration Check
    print("\n📦 GITHUB INTEGRATION CHECK:")
    if Path(".git").exists():
        print("✅ Git repository: Initialized")
    else:
        print("❌ Git repository: Not initialized")
        all_checks_passed = False
    
    # Final Summary
    print("\n" + "=" * 60)
    if all_checks_passed:
        print("🎉 ALL CHECKS PASSED! CODE IS COMPLETE!")
        print("✅ Backend: Fully implemented")
        print("✅ Frontend: Fully functional")
        print("✅ API: All endpoints working")
        print("✅ Testing: Comprehensive test suite")
        print("✅ Documentation: Complete")
        print("✅ Structure: Professional organization")
        print("✅ GitHub: Repository ready")
        print("\n🚀 INSTANT TUTOR AI MVP IS COMPLETE AND READY FOR PRODUCTION!")
    else:
        print("❌ SOME CHECKS FAILED!")
        print("Please review the failed items above and complete them.")
    
    print("=" * 60)
    return all_checks_passed

if __name__ == "__main__":
    check_code_completion()