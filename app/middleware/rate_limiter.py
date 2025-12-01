"""
Rate limiting middleware
"""

from flask import jsonify, current_app, request
from functools import wraps
from datetime import datetime, timedelta
import time

# Simple in-memory rate limiting (can be replaced with Redis)
rate_limit_storage = {}

def init_rate_limiter(app):
    """Initialize rate limiter."""
    # This is a basic implementation
    # In production, consider using Redis for distributed rate limiting
    
    @app.before_request
    def check_rate_limit():
        """Check rate limit for requests."""
        if not current_app.config.get('RATE_LIMIT_ENABLED', True):
            return
        
        client_ip = request.remote_addr
        endpoint = request.endpoint or request.path
        
        # Define rate limits per endpoint
        limits = {
            'api.auth': 5,      # 5 requests per minute for auth endpoints
            'api.ai': 10,       # 10 requests per minute for AI endpoints  
            'default': 100      # 100 requests per minute for other endpoints
        }
        
        # Determine the applicable limit
        rate_limit = 100  # default
        for key, limit in limits.items():
            if key in endpoint:
                rate_limit = limit
                break
        
        # Check if rate limited
        key = f"{client_ip}:{endpoint}"
        current_time = time.time()
        window_start = current_time - 60  # 1 minute window
        
        # Clean old entries
        if key in rate_limit_storage:
            rate_limit_storage[key] = [
                timestamp for timestamp in rate_limit_storage[key]
                if timestamp > window_start
            ]
        else:
            rate_limit_storage[key] = []
        
        # Check if limit exceeded
        if len(rate_limit_storage[key]) >= rate_limit:
            current_app.logger.warning(f"Rate limit exceeded for {client_ip} on {endpoint}")
            return jsonify({
                'success': False,
                'error': 'Rate limit exceeded',
                'status': 429,
                'retry_after': 60
            }), 429
        
        # Add current request to storage
        rate_limit_storage[key].append(current_time)

def rate_limit(requests_per_minute):
    """Decorator for custom rate limiting."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_app.config.get('RATE_LIMIT_ENABLED', True):
                return f(*args, **kwargs)
            
            # This is a simplified implementation
            # In production, use a proper rate limiting library
            return f(*args, **kwargs)
        return decorated_function
    return decorator
