"""
JWT Utilities for Instant Tutor AI
Secure token generation and validation
"""

import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

# JWT Configuration
JWT_SECRET_KEY = "pOEuZNr6WBoACKY8d98ddyp1Jugtpqu7Jel7O0PIP24JcB46w2Nod_zbJvlPa8aab4wicrGyRZubRPzTkoVnyg"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

class JWTManager:
    """JWT token management for Instant Tutor AI"""
    
    def __init__(self, secret_key: str = JWT_SECRET_KEY, algorithm: str = JWT_ALGORITHM):
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def create_user_tokens(self, user_id: str, user_type: str = "student", permissions: list = None) -> Dict[str, str]:
        """Create both access and refresh tokens for a user"""
        if permissions is None:
            permissions = ["read"]
        
        token_data = {
            "user_id": user_id,
            "user_type": user_type,
            "permissions": permissions,
            "iat": datetime.utcnow()
        }
        
        access_token = self.create_access_token(token_data)
        refresh_token = self.create_refresh_token(token_data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }

# Global JWT manager instance
jwt_manager = JWTManager()

def create_student_token(student_id: str, course_ids: list = None) -> Dict[str, str]:
    """Create tokens for a student user"""
    permissions = ["read", "query"]
    if course_ids:
        permissions.append("course_access")
    
    return jwt_manager.create_user_tokens(
        user_id=student_id,
        user_type="student",
        permissions=permissions
    )

def create_instructor_token(instructor_id: str, course_ids: list = None) -> Dict[str, str]:
    """Create tokens for an instructor user"""
    permissions = ["read", "query", "upload", "analytics"]
    if course_ids:
        permissions.append("course_management")
    
    return jwt_manager.create_user_tokens(
        user_id=instructor_id,
        user_type="instructor",
        permissions=permissions
    )

def create_admin_token(admin_id: str) -> Dict[str, str]:
    """Create tokens for an admin user"""
    return jwt_manager.create_user_tokens(
        user_id=admin_id,
        user_type="admin",
        permissions=["read", "query", "upload", "analytics", "admin", "manage_users"]
    )

def verify_access_token(token: str) -> Dict[str, Any]:
    """Verify access token and return payload"""
    payload = jwt_manager.verify_token(token)
    
    # Check if it's an access token
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload

def refresh_access_token(refresh_token: str) -> Dict[str, str]:
    """Refresh access token using refresh token"""
    payload = jwt_manager.verify_token(refresh_token)
    
    # Check if it's a refresh token
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create new access token
    token_data = {
        "user_id": payload["user_id"],
        "user_type": payload["user_type"],
        "permissions": payload["permissions"],
        "iat": datetime.utcnow()
    }
    
    access_token = jwt_manager.create_access_token(token_data)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

# Example usage functions
def demo_token_generation():
    """Demo function showing token generation"""
    print("🔐 JWT Token Generation Demo")
    print("=" * 40)
    
    # Student token
    student_tokens = create_student_token("student_123", ["MATH_101", "PHYSICS_101"])
    print("Student Tokens:")
    print(f"Access Token: {student_tokens['access_token'][:50]}...")
    print(f"Expires in: {student_tokens['expires_in']} seconds")
    
    # Instructor token
    instructor_tokens = create_instructor_token("instructor_456", ["MATH_101"])
    print("\nInstructor Tokens:")
    print(f"Access Token: {instructor_tokens['access_token'][:50]}...")
    print(f"Permissions: {instructor_tokens.get('permissions', 'N/A')}")
    
    # Admin token
    admin_tokens = create_admin_token("admin_789")
    print("\nAdmin Tokens:")
    print(f"Access Token: {admin_tokens['access_token'][:50]}...")
    print(f"User Type: admin")

if __name__ == "__main__":
    demo_token_generation()
