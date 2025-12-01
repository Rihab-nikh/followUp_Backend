"""
Configuration management for FollowUp API
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-super-secret-key-here'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    
    # Database settings
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/followup_db'
    
    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your-jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 900))  # 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 604800))  # 7 days
    
    # Gemini AI settings
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-1.5-flash')
    
    # CORS settings
    # Comma-separated list of allowed frontend origins for CORS.
    # Example: 'http://localhost:3000,https://v0-extractedfrontend.vercel.app'
    FRONTEND_ORIGINS = os.environ.get(
        'FRONTEND_ORIGINS',
        'http://localhost:3000,https://v0-extractedfrontend.vercel.app'
    )
    
    # Rate limiting
    RATE_LIMIT_ENABLED = os.environ.get('RATE_LIMIT_ENABLED', 'True').lower() == 'true'
    RATE_LIMIT_STORAGE_URL = os.environ.get('RATE_LIMIT_STORAGE_URL', 'memory://')
    
    # Email settings (optional)
    SMTP_HOST = os.environ.get('SMTP_HOST')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USER = os.environ.get('SMTP_USER')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')

class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    FLASK_ENV = 'production'
    
    # More secure settings for production
    JWT_ACCESS_TOKEN_EXPIRES = 900  # 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = 604800  # 7 days

class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/followup_test_db'
    JWT_ACCESS_TOKEN_EXPIRES = 60  # 1 minute for tests
    JWT_REFRESH_TOKEN_EXPIRES = 300  # 5 minutes for tests

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
