#!/usr/bin/env python3
"""
Instant Tutor AI - Main Entry Point
AI-powered tutoring system for Kerala education
"""

import sys
import os
from pathlib import Path

# Add backend to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from backend.api.main import app
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Instant Tutor AI...")
    print("📍 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔐 Health Check: http://localhost:8000/health")
    print("=" * 50)
    
    uvicorn.run(
        "backend.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
