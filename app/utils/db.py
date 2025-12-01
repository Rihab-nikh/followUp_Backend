"""
MongoDB database connection and utilities
"""

from flask import current_app
from datetime import datetime
import os

_db_client = None
_db = None

def init_db(app):
    """Initialize MongoDB connection or use mock database."""
    global _db_client, _db
    
    # Try to use real MongoDB first
    try:
        from pymongo import MongoClient
        _db_client = MongoClient(app.config['MONGO_URI'], 
                               serverSelectionTimeoutMS=5000,
                               connectTimeoutMS=5000)
        
        # Test connection
        _db_client.admin.command('ping')
        
        # Get database
        db_name = app.config['MONGO_URI'].split('/')[-1]
        _db = _db_client[db_name]
        
        # Store in app context
        app.db = _db
        
        app.logger.info("MongoDB connection initialized successfully")
        
    except Exception as e:
        # Fall back to mock database for development
        app.logger.warning(f"MongoDB connection failed: {e}")
        app.logger.info("Using mock in-memory database for development")
        
        from .mock_db import get_mock_db
        _db = get_mock_db()
        app.db = _db
        app.using_mock_db = True

def get_db():
    """Get database instance."""
    global _db
    if _db is None:
        raise RuntimeError("Database not initialized")
    return _db

def normalize_id(id_value):
    """
    Normalize ID values for database queries.
    Handles both MongoDB ObjectIds and UUID strings for mock database.
    """
    if hasattr(current_app, 'using_mock_db') and current_app.using_mock_db:
        # For mock database, use string IDs directly
        if not isinstance(id_value, str):
            return str(id_value)
        return id_value
    else:
        # For MongoDB, convert to ObjectId
        if isinstance(id_value, str):
            try:
                from bson import ObjectId
                return ObjectId(id_value)
            except Exception:
                # If conversion fails, use string as is
                return id_value
        return id_value

def close_db():
    """Close database connection."""
    global _db_client
    if _db_client:
        _db_client.close()

def get_collection(collection_name):
    """Get a MongoDB collection."""
    return get_db()[collection_name]

def create_indexes():
    """Create database indexes for performance."""
    try:
        # Users collection indexes
        users = get_collection('users')
        users.create_index('email', unique=True)
        
        # Meetings collection indexes
        meetings = get_collection('meetings')
        meetings.create_index('user_id')
        meetings.create_index('date')
        meetings.create_index('status')
        meetings.create_index([('company', 'text'), ('contact', 'text'), ('subject', 'text')])
        
        # Tasks collection indexes
        tasks = get_collection('tasks')
        tasks.create_index('user_id')
        tasks.create_index('due_date')
        tasks.create_index('status')
        tasks.create_index('assignee')
        
        # Notifications collection indexes
        notifications = get_collection('notifications')
        notifications.create_index('user_id')
        notifications.create_index('created_at')
        notifications.create_index('read')
        
        # AI chat collection indexes
        ai_chat = get_collection('ai_chat')
        ai_chat.create_index('user_id')
        ai_chat.create_index('session_id')
        
        # KPI metrics collection indexes
        kpi_metrics = get_collection('kpi_metrics')
        kpi_metrics.create_index('user_id')
        kpi_metrics.create_index('date')
        
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to create indexes: {e}")
        return False
