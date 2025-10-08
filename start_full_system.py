#!/usr/bin/env python3
"""
Complete system startup script for Instant Tutor AI
Starts both backend API and frontend server
"""

import subprocess
import time
import threading
import webbrowser
import requests
import sys
import os
from pathlib import Path

def check_backend_health():
    """Check if backend is running and healthy"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_backend():
    """Start the backend API server"""
    print("🚀 Starting Backend API...")
    try:
        # Start backend in a separate process
        process = subprocess.Popen([
            sys.executable, "start.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait for backend to start
        print("⏳ Waiting for backend to start...")
        for i in range(30):  # Wait up to 30 seconds
            if check_backend_health():
                print("✅ Backend API is running!")
                return process
            time.sleep(1)
            print(f"   Checking... ({i+1}/30)")
        
        print("❌ Backend failed to start within 30 seconds")
        return None
        
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def start_frontend():
    """Start the frontend server"""
    print("🌐 Starting Frontend Server...")
    try:
        # Start frontend server
        process = subprocess.Popen([
            sys.executable, "serve_frontend.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a moment for server to start
        time.sleep(3)
        print("✅ Frontend server is running!")
        return process
        
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None

def main():
    """Main startup function"""
    print("🎉 INSTANT TUTOR AI - COMPLETE SYSTEM STARTUP")
    print("=" * 60)
    print("🚀 Starting both Backend API and Frontend Server...")
    print("=" * 60)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend. Exiting.")
        return False
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend. Exiting.")
        backend_process.terminate()
        return False
    
    print("\n🎉 SYSTEM STARTUP COMPLETE!")
    print("=" * 60)
    print("📍 Backend API: http://localhost:8000")
    print("📍 Frontend: http://localhost:3000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔐 Health Check: http://localhost:8000/health")
    print("=" * 60)
    print("🔄 Press Ctrl+C to stop both servers")
    print("=" * 60)
    
    try:
        # Keep both processes running
        while True:
            time.sleep(1)
            
            # Check if backend is still running
            if backend_process.poll() is not None:
                print("❌ Backend process stopped unexpectedly")
                break
                
            # Check if frontend is still running
            if frontend_process.poll() is not None:
                print("❌ Frontend process stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n👋 Shutting down servers...")
        
        # Terminate both processes
        if backend_process:
            backend_process.terminate()
            print("✅ Backend stopped")
            
        if frontend_process:
            frontend_process.terminate()
            print("✅ Frontend stopped")
            
        print("👋 All servers stopped. Goodbye!")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
