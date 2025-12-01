"""
Request logging middleware
"""

from flask import request, current_app
from datetime import datetime
import json

def init_logging(app):
    """Initialize request logging."""
    
    @app.before_request
    def log_request_start():
        """Log request start."""
        if not current_app.debug:
            return
        
        start_time = datetime.utcnow()
        request.start_time = start_time
        
        # Log request details
        current_app.logger.info(
            f"REQUEST START - {request.method} {request.path} - "
            f"IP: {request.remote_addr} - "
            f"User-Agent: {request.headers.get('User-Agent', 'Unknown')}"
        )
    
    @app.after_request
    def log_request_end(response):
        """Log request completion."""
        if not current_app.debug or not hasattr(request, 'start_time'):
            return
        
        end_time = datetime.utcnow()
        duration = (end_time - request.start_time).total_seconds() * 1000
        
        # Log response details
        current_app.logger.info(
            f"REQUEST END - {request.method} {request.path} - "
            f"Status: {response.status_code} - "
            f"Duration: {duration:.2f}ms"
        )
        
        return response
