"""
JWT Authentication Middleware
"""

from functools import wraps
from flask import request, jsonify, current_app
from ..utils.jwt_helper import decode_token
from ..models.user import User

def init_auth_middleware(app):
    """Initialize authentication middleware."""
    @app.before_request
    def check_authentication():
        # Allow CORS preflight requests to proceed without authentication
        if request.method == 'OPTIONS':
            return
        # Skip authentication for public routes
        public_routes = [
            '/api/auth/login',
            '/api/auth/register',
            '/api/auth/refresh',
            '/api/health',
            '/api/auth/forgot-password',
            '/api/auth/reset-password'
        ]
        
        if request.path in public_routes:
            return
        
        # Check for authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'error': 'Authorization token required',
                'status': 401
            }), 401
        
        token = auth_header.split(' ')[1]
        
        # Decode and verify token
        payload = decode_token(token, 'access')
        if not payload:
            return jsonify({
                'success': False,
                'error': 'Invalid or expired token',
                'status': 401
            }), 401
        
        # Get user from database
        user = User.find_by_id(payload['user_id'])
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found',
                'status': 401
            }), 401
        
        # Attach user to request context
        request.user = user
        request.user_id = user.id if hasattr(user, 'id') else str(user._id)

def require_auth(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(request, 'user'):
            return jsonify({
                'success': False,
                'error': 'Authentication required',
                'status': 401
            }), 401
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(request, 'user'):
            return jsonify({
                'success': False,
                'error': 'Authentication required',
                'status': 401
            }), 401
        
        if request.user.role != 'admin':
            return jsonify({
                'success': False,
                'error': 'Admin access required',
                'status': 403
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

def require_admin_or_self(user_id_param='user_id'):
    """Decorator to require admin role or self-access."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(request, 'user'):
                return jsonify({
                    'success': False,
                    'error': 'Authentication required',
                    'status': 401
                }), 401
            
            # Get user_id from kwargs
            user_id = kwargs.get(user_id_param)
            
            # Allow access if user is admin or accessing their own data
            if request.user.role != 'admin' and request.user_id != user_id:
                return jsonify({
                    'success': False,
                    'error': 'Access denied. Admin or self-access required',
                    'status': 403
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_current_user_id():
    """Get the current authenticated user's ID."""
    if hasattr(request, 'user_id'):
        return request.user_id
    return None
