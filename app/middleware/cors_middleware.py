"""
CORS configuration middleware
"""

from flask import current_app, request
from flask_cors import cross_origin


def _parse_origins(origins):
    """Return a list of origins from a string or list stored in config."""
    if isinstance(origins, str):
        return [o.strip() for o in origins.split(',') if o.strip()]
    if isinstance(origins, (list, tuple)):
        return list(origins)
    return []

def init_cors(app):
    """Initialize CORS configuration."""
    @app.after_request
    def after_request(response):
        """Add CORS headers to all responses.

        When multiple allowed origins are configured, echo back the request's
        Origin header if it's in the allowed list. This avoids setting
        Access-Control-Allow-Origin to '*' when credentials are used.
        """
        allowed = _parse_origins(current_app.config.get('FRONTEND_ORIGINS', 'http://localhost:3000,https://v0-extractedfrontend.vercel.app'))
        origin = request.headers.get('Origin')

        if origin and origin in allowed:
            response.headers['Access-Control-Allow-Origin'] = origin
        else:
            # Fallback: if in debug, allow localhost; otherwise, leave unset
            if current_app.config.get('DEBUG', False) and 'http://localhost:3000' in allowed:
                response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'

        # Set common CORS headers
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Max-Age'] = '86400'  # 24 hours

        return response
    
    # For manual cross-origin requests
    def cors_route(*args, **kwargs):
        """Decorator for manual CORS handling using configured origins."""
        allowed = _parse_origins(current_app.config.get('FRONTEND_ORIGINS', 'http://localhost:3000,https://v0-extractedfrontend.vercel.app'))

        def decorator(func):
            return cross_origin(origins=allowed)(func)

        return decorator
