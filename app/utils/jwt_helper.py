"""
JWT token utilities for authentication
"""

import jwt
from datetime import datetime, timedelta
from flask import current_app

def generate_access_token(user_id):
    """Generate JWT access token."""
    payload = {
        'user_id': user_id,
        'type': 'access',
        'exp': datetime.utcnow() + timedelta(seconds=current_app.config['JWT_ACCESS_TOKEN_EXPIRES']),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def generate_refresh_token(user_id):
    """Generate JWT refresh token."""
    payload = {
        'user_id': user_id,
        'type': 'refresh',
        'exp': datetime.utcnow() + timedelta(seconds=current_app.config['JWT_REFRESH_TOKEN_EXPIRES']),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def decode_token(token, token_type='access'):
    """Decode and validate JWT token."""
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        
        # Verify token type
        if payload.get('type') != token_type:
            return None
        
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def is_token_expired(token):
    """Check if token is expired."""
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        exp = payload.get('exp')
        return datetime.utcnow() >= datetime.fromtimestamp(exp)
    except:
        return True

def get_token_expiry(token):
    """Get token expiry timestamp."""
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload.get('exp')
    except:
        return None
