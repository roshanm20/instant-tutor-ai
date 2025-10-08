"""
Database connection management for Kerala AI Tutor
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from typing import Generator

# Database URL configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{os.getenv('POSTGRES_USER', 'postgres')}:{os.getenv('POSTGRES_PASSWORD', 'password')}"
    f"@{os.getenv('POSTGRES_HOST', 'localhost')}/{os.getenv('POSTGRES_DB', 'kerala_tutor')}"
)

# For development, use SQLite if PostgreSQL is not available
if "postgresql" in DATABASE_URL and not os.getenv("POSTGRES_HOST"):
    DATABASE_URL = "sqlite:///./kerala_tutor.db"

# Create engine with appropriate configuration
if "sqlite" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Create all database tables
    """
    from .models import Base
    Base.metadata.create_all(bind=engine)

def init_database():
    """
    Initialize database with sample data
    """
    from .models import Class, Subject, Chapter, Section, Question
    
    create_tables()
    
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Class).first():
            print("Database already initialized")
            return
        
        # Create sample classes
        classes_data = [
            {"name": "Class 8", "description": "Kerala SCERT Class 8"},
            {"name": "Class 9", "description": "Kerala SCERT Class 9"},
            {"name": "Class 10", "description": "Kerala SCERT Class 10"},
            {"name": "Class 11", "description": "Kerala SCERT Class 11"},
            {"name": "Class 12", "description": "Kerala SCERT Class 12"},
        ]
        
        for class_data in classes_data:
            class_obj = Class(**class_data)
            db.add(class_obj)
        
        db.commit()
        
        # Create sample subjects for Class 10
        class_10 = db.query(Class).filter(Class.name == "Class 10").first()
        subjects_data = [
            {"name": "Mathematics", "class_id": class_10.id, "description": "Class 10 Mathematics"},
            {"name": "Physics", "class_id": class_10.id, "description": "Class 10 Physics"},
            {"name": "Chemistry", "class_id": class_10.id, "description": "Class 10 Chemistry"},
            {"name": "Biology", "class_id": class_10.id, "description": "Class 10 Biology"},
        ]
        
        for subject_data in subjects_data:
            subject_obj = Subject(**subject_data)
            db.add(subject_obj)
        
        db.commit()
        
        # Create sample chapters for Mathematics
        math_subject = db.query(Subject).filter(Subject.name == "Mathematics").first()
        chapters_data = [
            {"name": "Linear Equations in Two Variables", "subject_id": math_subject.id, "chapter_number": 1},
            {"name": "Quadratic Equations", "subject_id": math_subject.id, "chapter_number": 2},
            {"name": "Arithmetic Progressions", "subject_id": math_subject.id, "chapter_number": 3},
        ]
        
        for chapter_data in chapters_data:
            chapter_obj = Chapter(**chapter_data)
            db.add(chapter_obj)
        
        db.commit()
        
        # Create sample sections for Linear Equations
        linear_chapter = db.query(Chapter).filter(Chapter.name == "Linear Equations in Two Variables").first()
        sections_data = [
            {
                "title": "Introduction to Linear Equations",
                "content": "A linear equation in two variables is an equation of the form ax + by + c = 0, where a, b, and c are real numbers, and a and b are not both zero. The solution of a linear equation in two variables is a pair of values (x, y) that makes the equation true.",
                "chapter_id": linear_chapter.id,
                "section_number": 1,
                "difficulty_level": "easy"
            },
            {
                "title": "Graphical Method of Solving Linear Equations",
                "content": "The graphical method involves plotting the equation on a coordinate plane. The point of intersection of the two lines represents the solution. This method is useful for understanding the relationship between the variables.",
                "chapter_id": linear_chapter.id,
                "section_number": 2,
                "difficulty_level": "intermediate"
            },
            {
                "title": "Algebraic Method of Solving Linear Equations",
                "content": "The algebraic method involves using substitution or elimination to find the values of x and y. This method is more precise and can handle complex systems of equations.",
                "chapter_id": linear_chapter.id,
                "section_number": 3,
                "difficulty_level": "intermediate"
            }
        ]
        
        for section_data in sections_data:
            section_obj = Section(**section_data)
            db.add(section_obj)
        
        db.commit()
        
        print("Database initialized with sample data")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()
