"""
Database Models for Kerala AI Tutor
SQLAlchemy models for structured syllabus metadata storage
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Class(Base):
    """Classes/Standards (8th, 9th, 10th, 11th, 12th)"""
    __tablename__ = 'classes'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)  # "Class 10", "Class 11"
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    subjects = relationship("Subject", back_populates="class_ref")

class Subject(Base):
    """Subjects within each class (Math, Physics, Chemistry, etc.)"""
    __tablename__ = 'subjects'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # "Mathematics", "Physics"
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    class_ref = relationship("Class", back_populates="subjects")
    chapters = relationship("Chapter", back_populates="subject")

class Chapter(Base):
    """Chapters within each subject"""
    __tablename__ = 'chapters'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)  # "Linear Equations", "Quadratic Equations"
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    chapter_number = Column(Integer)  # Chapter sequence number
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    subject = relationship("Subject", back_populates="chapters")
    sections = relationship("Section", back_populates="chapter")

class Section(Base):
    """Sections within each chapter (main content for embedding)"""
    __tablename__ = 'sections'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)  # "Introduction to Linear Equations"
    content = Column(Text, nullable=False)  # Main content for embedding
    chapter_id = Column(Integer, ForeignKey('chapters.id'), nullable=False)
    section_number = Column(Integer)  # Section sequence within chapter
    difficulty_level = Column(String(20), default="intermediate")  # easy, intermediate, hard
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    chapter = relationship("Chapter", back_populates="sections")
    questions = relationship("Question", back_populates="section")

class Question(Base):
    """Sample questions and answers for each section"""
    __tablename__ = 'questions'
    
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=False)
    section_id = Column(Integer, ForeignKey('sections.id'), nullable=False)
    question_type = Column(String(50), default="short_answer")  # short_answer, long_answer, mcq
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    section = relationship("Section", back_populates="questions")

class QueryLog(Base):
    """Log all user queries for analytics and improvement"""
    __tablename__ = 'query_logs'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100))  # Anonymous user tracking
    query_text = Column(Text, nullable=False)
    course_id = Column(String(50))  # Which course/subject
    response_text = Column(Text)  # AI response
    confidence_score = Column(Float)  # AI confidence
    response_time_ms = Column(Integer)  # Response time in milliseconds
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_rating = Column(Integer)  # 1-5 rating from user
    feedback = Column(Text)  # User feedback

class UserSession(Base):
    """Track user sessions for analytics"""
    __tablename__ = 'user_sessions'
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, nullable=False)
    user_id = Column(String(100))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    total_queries = Column(Integer, default=0)
    course_focus = Column(String(100))  # Most queried course
    satisfaction_score = Column(Float)  # Average rating
