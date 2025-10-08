"""
Instant Tutor AI - Secure Configuration
Generated JWT Secret Key and Security Settings
"""

import os
import secrets
from datetime import timedelta

# Generated Secure JWT Secret Key
JWT_SECRET_KEY = "pOEuZNr6WBoACKY8d98ddyp1Jugtpqu7Jel7O0PIP24JcB46w2Nod_zbJvlPa8aab4wicrGyRZubRPzTkoVnyg"

# Security Configuration
SECURITY_CONFIG = {
    # JWT Settings
    "JWT_SECRET_KEY": JWT_SECRET_KEY,
    "JWT_ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": 60,
    "REFRESH_TOKEN_EXPIRE_DAYS": 7,
    
    # Password Security
    "PASSWORD_MIN_LENGTH": 8,
    "PASSWORD_REQUIRE_UPPERCASE": True,
    "PASSWORD_REQUIRE_LOWERCASE": True,
    "PASSWORD_REQUIRE_NUMBERS": True,
    "PASSWORD_REQUIRE_SPECIAL": True,
    
    # Rate Limiting
    "RATE_LIMIT_PER_MINUTE": 60,
    "RATE_LIMIT_PER_HOUR": 1000,
    "RATE_LIMIT_PER_DAY": 10000,
    
    # CORS Settings
    "CORS_ORIGINS": [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ],
    
    # Session Security
    "SESSION_COOKIE_SECURE": True,
    "SESSION_COOKIE_HTTPONLY": True,
    "SESSION_COOKIE_SAMESITE": "strict",
    
    # API Security
    "API_KEY_HEADER": "X-API-Key",
    "REQUIRE_API_KEY": True,
    
    # File Upload Security
    "MAX_FILE_SIZE": 500 * 1024 * 1024,  # 500MB
    "ALLOWED_VIDEO_FORMATS": ["mp4", "avi", "mov", "wmv"],
    "UPLOAD_FOLDER": "./uploads",
    
    # Database Security
    "DATABASE_POOL_SIZE": 10,
    "DATABASE_MAX_OVERFLOW": 20,
    "DATABASE_POOL_TIMEOUT": 30,
    "DATABASE_POOL_RECYCLE": 3600,
}

def generate_new_jwt_secret():
    """Generate a new secure JWT secret key"""
    return secrets.token_urlsafe(64)

def get_jwt_config():
    """Get JWT configuration for the application"""
    return {
        "secret_key": JWT_SECRET_KEY,
        "algorithm": SECURITY_CONFIG["JWT_ALGORITHM"],
        "access_token_expire_minutes": SECURITY_CONFIG["ACCESS_TOKEN_EXPIRE_MINUTES"],
        "refresh_token_expire_days": SECURITY_CONFIG["REFRESH_TOKEN_EXPIRE_DAYS"]
    }

def validate_jwt_secret(secret_key: str) -> bool:
    """Validate JWT secret key strength"""
    if not secret_key:
        return False
    if len(secret_key) < 32:
        return False
    return True

# Example usage in your FastAPI app:
"""
from secure_config import get_jwt_config, JWT_SECRET_KEY

# In your FastAPI app
jwt_config = get_jwt_config()
"""

if __name__ == "__main__":
    print("🔐 Instant Tutor AI - Security Configuration")
    print("=" * 50)
    print(f"JWT Secret Key: {JWT_SECRET_KEY}")
    print(f"Key Length: {len(JWT_SECRET_KEY)} characters")
    print(f"Algorithm: {SECURITY_CONFIG['JWT_ALGORITHM']}")
    print(f"Token Expiry: {SECURITY_CONFIG['ACCESS_TOKEN_EXPIRE_MINUTES']} minutes")
    print("\n✅ Secure configuration generated successfully!")
    print("\n📝 To use this in your application:")
    print("1. Copy the JWT_SECRET_KEY to your .env file")
    print("2. Import get_jwt_config() in your FastAPI app")
    print("3. Use the configuration for JWT token generation")
