"""
FollowUp Meeting Management Backend API
Flask application factory with MVC architecture and blueprints
"""

import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.config import Config
from app.utils.db import init_db
from app.middleware.auth_middleware import init_auth_middleware
from app.middleware.error_handler import init_error_handler
from app.middleware.cors_middleware import init_cors
from app.middleware.logging_middleware import init_logging
from app.middleware.rate_limiter import init_rate_limiter

def create_app(config_class=Config):
    """Application factory for Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    init_db(app)
    # Configure CORS origins: allow localhost and the Vercel frontend
    # Keep using config if provided (FRONTEND_ORIGINS can be comma-separated or a list)
    # Default explicitly includes the deployed Vercel URL used by the frontend.
    CORS(app, origins=[
        'http://localhost:3000',
        'https://v0-extractedfrontend.vercel.app'
    ])
    # NOTE: This project uses MongoDB (pymongo). Flask-Migrate is for SQLAlchemy
    # databases and will raise an error when passed a pymongo Database object.
    # If you later add SQLAlchemy, initialize Flask-Migrate with the SQLAlchemy
    # db instance (e.g. `Migrate(app, db)`). For now we skip Flask-Migrate.
    
    # Initialize middleware
    init_logging(app)
    init_error_handler(app)
    init_cors(app)
    init_rate_limiter(app)
    init_auth_middleware(app)
    
    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.meeting_routes import meeting_bp
    from app.routes.task_routes import task_bp
    from app.routes.notification_routes import notification_bp
    from app.routes.ai_routes import ai_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.settings_routes import settings_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(meeting_bp, url_prefix='/api/meetings')
    app.register_blueprint(task_bp, url_prefix='/api/tasks')
    app.register_blueprint(notification_bp, url_prefix='/api/notifications')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(settings_bp, url_prefix='/api/settings')
    
    # Health check endpoint
    @app.route('/api/health')
    def health_check():
        return {
            'success': True,
            'status': 'healthy',
            'message': 'FollowUp API is running',
            'version': '1.0.0'
        }
    
    return app
