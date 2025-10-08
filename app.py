# Kerala AI Tutor - Simplified FastAPI Application
# Minimal working version without heavy dependencies

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
import os
from datetime import datetime
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Kerala AI Tutor",
    description="AI-powered tutoring system for Kerala education",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pydantic models for API
class QueryRequest(BaseModel):
    query: str = Field(..., min_length=5, max_length=500, description="User's question")
    course_id: str = Field(..., description="Course identifier")
    user_id: Optional[str] = Field(None, description="User identifier")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")

class QueryResponse(BaseModel):
    answer: str = Field(..., description="AI-generated answer")
    sources: List[Dict[str, Any]] = Field(..., description="Source references")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Response confidence score")
    response_time: int = Field(..., description="Response time in milliseconds")
    suggested_followups: List[str] = Field(..., description="Suggested follow-up questions")

class CourseUploadRequest(BaseModel):
    course_id: str = Field(..., description="Unique course identifier")
    course_title: str = Field(..., description="Course title")
    video_urls: List[str] = Field(..., description="List of video URLs or paths")
    instructor_name: Optional[str] = Field(None, description="Instructor name")
    language: str = Field("english", description="Course language")
    difficulty: str = Field("intermediate", description="Course difficulty level")

class FeedbackRequest(BaseModel):
    query_id: int = Field(..., description="Query log ID")
    rating: int = Field(..., ge=1, le=5, description="Feedback rating (1-5)")
    comment: Optional[str] = Field(None, description="Optional feedback comment")

# Authentication dependency (simplified for MVP)
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != "demo-token-123":
        raise HTTPException(status_code=403, detail="Invalid authentication token")
    return {"user_id": "demo_user", "permissions": ["read", "write"]}

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "services": {
            "vector_db": "demo_mode",
            "ai_model": "demo_mode",
            "message": "Kerala AI Tutor is running in demo mode"
        }
    }

# Main Q&A endpoint
@app.post("/api/query", response_model=QueryResponse)
async def ask_question(
    request: QueryRequest,
    auth: Dict = Depends(verify_token)
):
    """Main endpoint for asking questions to the AI tutor"""
    start_time = datetime.utcnow()
    
    try:
        logger.info(f"Processing query: {request.query}")
        
        # Demo mode - generate intelligent responses
        demo_responses = {
            "calculus": {
                "answer": "The derivative of x² is 2x. This follows from the power rule: d/dx(x^n) = nx^(n-1). For x², we get 2x^(2-1) = 2x. This is a fundamental concept in calculus that you'll use throughout your studies.",
                "confidence": 0.95,
                "sources": [
                    {
                        "id": 1,
                        "content_preview": "Power rule for derivatives: d/dx(x^n) = nx^(n-1)...",
                        "video_path": "lectures/derivatives.mp4",
                        "timestamp": {"start": 120, "end": 180},
                        "relevance_score": 0.92,
                        "topic": "Derivatives"
                    }
                ],
                "followups": [
                    "What is the derivative of x³?",
                    "How do I find the derivative of more complex functions?",
                    "What is the chain rule in calculus?"
                ]
            },
            "physics": {
                "answer": "Newton's second law states that F = ma, where F is force, m is mass, and a is acceleration. This fundamental law relates the motion of an object to the forces acting upon it.",
                "confidence": 0.90,
                "sources": [
                    {
                        "id": 1,
                        "content_preview": "Newton's laws of motion form the foundation of classical mechanics...",
                        "video_path": "lectures/newton_laws.mp4",
                        "timestamp": {"start": 45, "end": 120},
                        "relevance_score": 0.88,
                        "topic": "Newton's Laws"
                    }
                ],
                "followups": [
                    "What are Newton's other laws?",
                    "How do I apply F=ma to solve problems?",
                    "What is the difference between mass and weight?"
                ]
            },
            "chemistry": {
                "answer": "The periodic table is organized by atomic number and shows periodic trends in properties. Elements in the same group have similar chemical properties due to their valence electron configuration.",
                "confidence": 0.88,
                "sources": [
                    {
                        "id": 1,
                        "content_preview": "The periodic table arranges elements by atomic number and reveals periodic trends...",
                        "video_path": "lectures/periodic_table.mp4",
                        "timestamp": {"start": 30, "end": 90},
                        "relevance_score": 0.85,
                        "topic": "Periodic Table"
                    }
                ],
                "followups": [
                    "What are the main groups in the periodic table?",
                    "How do atomic radius and electronegativity change across periods?",
                    "What is the significance of valence electrons?"
                ]
            }
        }
        
        # Simple keyword matching for demo
        query_lower = request.query.lower()
        if any(word in query_lower for word in ["derivative", "calculus", "x²", "x squared"]):
            response_data = demo_responses["calculus"]
        elif any(word in query_lower for word in ["newton", "force", "physics", "f=ma"]):
            response_data = demo_responses["physics"]
        elif any(word in query_lower for word in ["periodic", "table", "chemistry", "element"]):
            response_data = demo_responses["chemistry"]
        else:
            # Generic response
            response_data = {
                "answer": f"Based on your question about '{request.query}' in course {request.course_id}, here's what I found: This is a demo response showing how the AI tutor would provide instant, intelligent answers to your questions. In the full implementation, this would be powered by vector database search and advanced AI models.",
                "confidence": 0.75,
                "sources": [
                    {
                        "id": 1,
                        "content_preview": f"Demo content related to '{request.query}' in {request.course_id}...",
                        "video_path": "demo_video.mp4",
                        "timestamp": {"start": 0, "end": 300},
                        "relevance_score": 0.70,
                        "topic": "General"
                    }
                ],
                "followups": [
                    "Can you provide more details about this topic?",
                    "What are some practical examples?",
                    "How does this relate to other concepts in the course?"
                ]
            }
        
        # Calculate response time
        end_time = datetime.utcnow()
        response_time = int((end_time - start_time).total_seconds() * 1000)
        
        # Prepare response
        response = QueryResponse(
            answer=response_data["answer"],
            sources=response_data["sources"],
            confidence=response_data["confidence"],
            response_time=response_time,
            suggested_followups=response_data["followups"]
        )
        
        logger.info(f"Query processed in {response_time}ms")
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Course upload endpoint
@app.post("/api/courses/upload")
async def upload_course(
    request: CourseUploadRequest,
    auth: Dict = Depends(verify_token)
):
    """Upload and process course videos"""
    
    try:
        logger.info(f"Course upload initiated: {request.course_title}")
        
        # Demo mode - simulate processing
        return {
            "message": f"Course '{request.course_title}' upload initiated",
            "course_id": request.course_id,
            "status": "processing",
            "video_count": len(request.video_urls),
            "note": "Demo mode - videos would be processed with Whisper and stored in vector database"
        }
        
    except Exception as e:
        logger.error(f"Error initiating course upload: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate course upload")

# Feedback endpoint
@app.post("/api/feedback")
async def submit_feedback(
    request: FeedbackRequest,
    auth: Dict = Depends(verify_token)
):
    """Submit feedback for a query response"""
    
    try:
        logger.info(f"Feedback submitted for query {request.query_id}: {request.rating}/5")
        
        return {
            "message": "Feedback submitted successfully",
            "query_id": request.query_id,
            "rating": request.rating,
            "note": "Demo mode - feedback would be stored in database"
        }
        
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit feedback")

# Analytics endpoint
@app.get("/api/analytics/course/{course_id}")
async def get_course_analytics(
    course_id: str,
    auth: Dict = Depends(verify_token)
):
    """Get analytics for a specific course"""
    
    try:
        # Demo analytics
        return {
            "course_id": course_id,
            "total_queries": 42,
            "avg_response_time_ms": 1500,
            "avg_user_rating": 4.2,
            "knowledge_base": {
                "total_content_chunks": 156,
                "last_updated": datetime.utcnow().isoformat()
            },
            "note": "Demo analytics - real data would come from database"
        }
        
    except Exception as e:
        logger.error(f"Error getting course analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics")

# Kerala-specific features endpoint
@app.get("/api/kerala/features")
async def get_kerala_features():
    """Get Kerala-specific features and capabilities"""
    return {
        "language_support": ["English", "Malayalam", "Hindi"],
        "curriculum_alignment": ["SCERT", "CBSE", "ICSE"],
        "local_integrations": ["Edapt", "Avasarshala", "PowerSchool India"],
        "government_schemes": ["KSUM", "K-AI", "Digital Kerala"],
        "pricing": {
            "student_per_year": "₹100-200",
            "institution_savings": "30%+ cost reduction"
        }
    }

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
