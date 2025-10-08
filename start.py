#!/usr/bin/env python3
"""
Instant Tutor AI - Startup Script
Comprehensive startup with health checks and validation
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("=" * 60)
    print("🚀 INSTANT TUTOR AI - Kerala EdTech MVP")
    print("🤖 AI-Powered Tutoring System")
    print("📍 Built for Kerala's Education Future")
    print("=" * 60)

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import fastapi
        import uvicorn
        import pydantic
        print("✅ FastAPI dependencies: OK")
    except ImportError as e:
        print(f"❌ FastAPI dependencies missing: {e}")
        return False
    
    try:
        import openai
        print("✅ OpenAI: OK")
    except ImportError:
        print("⚠️  OpenAI: Not installed (optional)")
    
    try:
        import weaviate
        print("✅ Weaviate: OK")
    except ImportError:
        print("⚠️  Weaviate: Not installed (optional)")
    
    return True

def check_environment():
    """Check environment configuration"""
    print("🔧 Checking environment...")
    
    # Check if .env exists
    if not Path(".env").exists():
        print("⚠️  .env file not found. Using demo mode.")
        print("📝 Copy config/env.example to .env for production")
    else:
        print("✅ Environment file: OK")
    
    return True

def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting Instant Tutor AI Backend...")
    print("📍 API: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("🔐 Health: http://localhost:8000/health")
    print("=" * 60)
    
    try:
        # Start the backend
        subprocess.run([
            sys.executable, "main.py"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down Instant Tutor AI...")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False
    
    return True

def test_api():
    """Test API endpoints"""
    print("🧪 Testing API endpoints...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint: OK")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test query endpoint
        headers = {"Authorization": "Bearer demo-token-123"}
        data = {
            "query": "What is the derivative of x squared?",
            "course_id": "MATH_101",
            "user_id": "student_123"
        }
        
        response = requests.post(
            "http://localhost:8000/api/query",
            headers=headers,
            json=data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Query endpoint: OK")
        else:
            print(f"❌ Query endpoint failed: {response.status_code}")
            return False
        
        print("🎉 All API tests passed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure backend is running.")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    """Main startup function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed. Please install requirements:")
        print("   pip install -r requirements.txt")
        return
    
    # Check environment
    if not check_environment():
        print("❌ Environment check failed.")
        return
    
    print("✅ All checks passed!")
    print("🚀 Starting Instant Tutor AI...")
    
    # Start backend
    start_backend()

if __name__ == "__main__":
    main()
