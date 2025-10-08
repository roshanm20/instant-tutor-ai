# AI EdTech MVP - FastAPI Backend with Vector Database Integration
# Complete API implementation for AI-powered Q&A system

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import asyncio
import logging
import os
from datetime import datetime
import uvicorn

# Import our custom modules
from video_processor import CourseContentProcessor
from pinecone_setup import PineconeSetup
from weaviate_setup import WeaviateSetup

# Embedding and AI imports
from sentence_transformers import SentenceTransformer
import openai

# Database
from sqlalchemy import create_engine, Column, String, DateTime, Text, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI EdTech Q&A System",
    description="AI-powered tutoring system replacing weekly Q&A forums",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/edtech_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class QueryLog(Base):
    __tablename__ = "query_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    course_id = Column(String, index=True)
    query_text = Column(Text)
    response_text = Column(Text)
    response_time = Column(Integer)  # milliseconds
    timestamp = Column(DateTime, default=datetime.utcnow)
    feedback_score = Column(Integer, nullable=True)  # 1-5 rating

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models for API
class QueryRequest(BaseModel):
    query: str = Field(..., min_length=5, max_length=500, description="User's question")
    course_id: str = Field(..., description="Course identifier")
    user_id: Optional[str] = Field(None, description="User identifier for personalization")
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

# Global variables for initialized services
vector_db = None
embedding_model = None
course_processor = None

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication dependency (simplified for MVP)
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # In production, implement proper JWT token validation
    token = credentials.credentials
    if token != "demo-token-123":  # Replace with actual token validation
        raise HTTPException(status_code=403, detail="Invalid authentication token")
    return {"user_id": "demo_user", "permissions": ["read", "write"]}

# Initialize services
@app.on_event("startup")
async def startup_event():
    """Initialize AI services on startup"""
    global vector_db, embedding_model, course_processor
    
    try:
        # Initialize embedding model
        logger.info("Loading embedding model...")
        embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize vector database (Weaviate for MVP)
        logger.info("Connecting to vector database...")
        try:
            vector_db = WeaviateSetup(
                url=os.getenv("WEAVIATE_URL", "http://localhost:8080"),
                api_key=os.getenv("WEAVIATE_API_KEY")
            )
            # Create schema if not exists
            vector_db.create_course_schema()
            logger.info("Weaviate connected successfully")
        except Exception as weaviate_error:
            logger.warning(f"Could not connect to Weaviate: {weaviate_error}")
            logger.info("Running in demo mode without vector database")
            vector_db = None
        
        # Initialize course processor
        config = {
            "vector_db": "weaviate" if vector_db else "demo",
            "whisper_model": "base",
            "embedding_model": "all-MiniLM-L6-v2",
            "chunk_size": 1000,
            "chunk_overlap": 200,
            "weaviate_url": os.getenv("WEAVIATE_URL", "http://localhost:8080"),
            "openai_api_key": os.getenv("OPENAI_API_KEY")
        }
        course_processor = CourseContentProcessor(config)
        
        logger.info("All services initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        # Don't raise, allow app to start in demo mode
        logger.info("Starting in demo mode...")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global vector_db
    if vector_db:
        vector_db.close_connection()

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "services": {
            "vector_db": "connected" if vector_db else "disconnected",
            "embedding_model": "loaded" if embedding_model else "not_loaded"
        }
    }

# Main Q&A endpoint
@app.post("/api/query", response_model=QueryResponse)
async def ask_question(
    request: QueryRequest,
    db: Session = Depends(get_db),
    auth: Dict = Depends(verify_token)
):
    """Main endpoint for asking questions to the AI tutor"""
    start_time = datetime.utcnow()
    
    try:
        # Log the query
        query_log = QueryLog(
            user_id=request.user_id or auth["user_id"],
            course_id=request.course_id,
            query_text=request.query,
            timestamp=start_time
        )
        db.add(query_log)
        db.commit()
        
        # Search for relevant content in vector database
        logger.info(f"Searching for content related to: {request.query}")
        
        if vector_db:
            search_results = vector_db.search_course_content(
                collection_name="CourseContent",
                query=request.query,
                course_filter=request.course_id,
                limit=5
            )
        else:
            # Demo mode - return mock results
            search_results = [
                {
                    "content": f"Demo content related to '{request.query}' in course {request.course_id}. This is a sample response for demonstration purposes.",
                    "course_id": request.course_id,
                    "video_path": "demo_video.mp4",
                    "start_time": 0,
                    "end_time": 300,
                    "certainty": 0.8
                }
            ]
        
        # Generate AI response based on retrieved content
        ai_response = await generate_ai_response(
            query=request.query,
            context_results=search_results,
            course_id=request.course_id
        )
        
        # Calculate response time
        end_time = datetime.utcnow()
        response_time = int((end_time - start_time).total_seconds() * 1000)
        
        # Update query log with response
        query_log.response_text = ai_response["answer"]
        query_log.response_time = response_time
        db.commit()
        
        # Prepare response
        response = QueryResponse(
            answer=ai_response["answer"],
            sources=format_sources(search_results),
            confidence=ai_response["confidence"],
            response_time=response_time,
            suggested_followups=ai_response.get("followups", [])
        )
        
        logger.info(f"Query processed in {response_time}ms")
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def generate_ai_response(query: str, context_results: List[Dict], course_id: str) -> Dict[str, Any]:
    """Generate AI response using OpenAI or fallback to template-based response"""
    
    # Prepare context from search results
    context_text = "\n\n".join([
        f"Content {i+1}: {result['content'][:500]}..." 
        for i, result in enumerate(context_results[:3])
    ])
    
    # Calculate confidence based on search results relevance
    avg_score = sum(result.get('certainty', 0.5) for result in context_results) / max(len(context_results), 1)
    confidence = min(avg_score, 0.95)  # Cap at 95%
    
    try:
        # Try OpenAI API first
        if os.getenv("OPENAI_API_KEY"):
            openai.api_key = os.getenv("OPENAI_API_KEY")
            
            prompt = f"""
            You are an AI tutor helping students understand course material. Based on the provided context from course videos, answer the student's question clearly and concisely.

            Student Question: {query}

            Course Context:
            {context_text}

            Instructions:
            1. Provide a clear, educational answer based on the context
            2. If the context doesn't contain enough information, say so honestly
            3. Include specific references to the course material when possible
            4. Keep the answer focused and helpful for learning
            5. Suggest related topics the student might want to explore

            Answer:
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Generate follow-up questions
            followup_prompt = f"Based on the question '{query}' and this answer: '{answer}', suggest 3 related follow-up questions a student might ask:"
            
            followup_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": followup_prompt}],
                max_tokens=150,
                temperature=0.8
            )
            
            followups = [
                line.strip().lstrip('1234567890.-').strip() 
                for line in followup_response.choices[0].message.content.split('\n')
                if line.strip()
            ][:3]
            
            return {
                "answer": answer,
                "confidence": confidence,
                "followups": followups
            }
            
    except Exception as e:
        logger.warning(f"OpenAI API failed, using fallback: {e}")
    
    # Fallback to template-based response
    if context_results:
        answer = f"Based on the course material, here's what I found related to your question:\n\n"
        answer += context_results[0]['content'][:400] + "..."
        
        if len(context_results) > 1:
            answer += f"\n\nAdditionally, you might want to review the section that discusses: {context_results[1]['topic']}"
    else:
        answer = f"I couldn't find specific information about '{query}' in the current course materials. Please try rephrasing your question or contact your instructor for clarification."
    
    followups = [
        "Can you provide more details about this topic?",
        "What are some practical examples of this concept?",
        "How does this relate to other topics in the course?"
    ]
    
    return {
        "answer": answer,
        "confidence": max(confidence * 0.7, 0.3),  # Lower confidence for fallback
        "followups": followups
    }

def format_sources(search_results: List[Dict]) -> List[Dict[str, Any]]:
    """Format search results as source references"""
    sources = []
    
    for i, result in enumerate(search_results[:3]):
        source = {
            "id": i + 1,
            "content_preview": result['content'][:150] + "..." if len(result['content']) > 150 else result['content'],
            "video_path": result.get('video_path', ''),
            "timestamp": {
                "start": result.get('start_time', 0),
                "end": result.get('end_time', 0)
            },
            "relevance_score": result.get('certainty', result.get('score', 0.5)),
            "topic": result.get('topic', 'General')
        }
        sources.append(source)
    
    return sources

# Course upload endpoint
@app.post("/api/courses/upload")
async def upload_course(
    request: CourseUploadRequest,
    background_tasks: BackgroundTasks,
    auth: Dict = Depends(verify_token)
):
    """Upload and process course videos"""
    
    try:
        # Add background task to process videos
        background_tasks.add_task(
            process_course_videos,
            course_id=request.course_id,
            video_urls=request.video_urls,
            course_metadata={
                "title": request.course_title,
                "instructor": request.instructor_name,
                "language": request.language,
                "difficulty": request.difficulty
            }
        )
        
        return {
            "message": f"Course '{request.course_title}' upload initiated",
            "course_id": request.course_id,
            "status": "processing",
            "video_count": len(request.video_urls)
        }
        
    except Exception as e:
        logger.error(f"Error initiating course upload: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate course upload")

async def process_course_videos(course_id: str, video_urls: List[str], course_metadata: Dict[str, Any]):
    """Background task to process course videos"""
    try:
        logger.info(f"Starting processing for course {course_id}")
        
        # Process videos using our course processor
        success = await course_processor.process_course_videos(video_urls, course_id)
        
        if success:
            logger.info(f"Successfully processed course {course_id}")
        else:
            logger.error(f"Failed to process course {course_id}")
            
    except Exception as e:
        logger.error(f"Error in background video processing: {e}")

# Feedback endpoint
@app.post("/api/feedback")
async def submit_feedback(
    request: FeedbackRequest,
    db: Session = Depends(get_db),
    auth: Dict = Depends(verify_token)
):
    """Submit feedback for a query response"""
    
    try:
        # Find the query log entry
        query_log = db.query(QueryLog).filter(QueryLog.id == request.query_id).first()
        
        if not query_log:
            raise HTTPException(status_code=404, detail="Query not found")
        
        # Update with feedback
        query_log.feedback_score = request.rating
        db.commit()
        
        logger.info(f"Feedback submitted for query {request.query_id}: {request.rating}/5")
        
        return {
            "message": "Feedback submitted successfully",
            "query_id": request.query_id,
            "rating": request.rating
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit feedback")

# Analytics endpoint
@app.get("/api/analytics/course/{course_id}")
async def get_course_analytics(
    course_id: str,
    db: Session = Depends(get_db),
    auth: Dict = Depends(verify_token)
):
    """Get analytics for a specific course"""
    
    try:
        # Query analytics from database
        total_queries = db.query(QueryLog).filter(QueryLog.course_id == course_id).count()
        
        avg_response_time = db.query(QueryLog).filter(
            QueryLog.course_id == course_id,
            QueryLog.response_time.isnot(None)
        ).with_entities(
            db.func.avg(QueryLog.response_time)
        ).scalar() or 0
        
        avg_feedback = db.query(QueryLog).filter(
            QueryLog.course_id == course_id,
            QueryLog.feedback_score.isnot(None)
        ).with_entities(
            db.func.avg(QueryLog.feedback_score)
        ).scalar() or 0
        
        # Get vector database stats
        collection_stats = vector_db.get_collection_stats("CourseContent")
        
        return {
            "course_id": course_id,
            "total_queries": total_queries,
            "avg_response_time_ms": int(avg_response_time),
            "avg_user_rating": round(float(avg_feedback), 2),
            "knowledge_base": {
                "total_content_chunks": collection_stats.get("total_objects", 0),
                "last_updated": datetime.utcnow().isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting course analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analytics")

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )