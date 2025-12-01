"""
Authentication controller for user registration, login, and token management
"""

from flask import jsonify, current_app, request
from marshmallow import ValidationError
from ..models.user import User
from ..schemas.user_schema import (
    UserRegisterSchema, UserLoginSchema, UserUpdateSchema,
    PasswordChangeSchema, PasswordResetSchema, PasswordResetConfirmSchema
)
from ..utils.password_helper import hash_password, verify_password, generate_reset_token, validate_password_strength
from ..utils.jwt_helper import generate_access_token, generate_refresh_token, decode_token
from ..utils.validators import validate_email_address
from datetime import datetime

class AuthController:
    """Authentication controller for user management."""
    
    @staticmethod
    def _get_user_id(user):
        """Return a string user id from a User object, safely handling missing attrs."""
        # Prefer `id` attribute if present (already a string), otherwise try `_id` and convert.
        user_id = getattr(user, 'id', None)
        if user_id:
            return user_id
        _id = getattr(user, '_id', None)
        if _id is None:
            return None
        try:
            return str(_id)
        except Exception:
            return None
    @staticmethod
    def register():
        """Register a new user."""
        try:
            # Validate request data
            schema = UserRegisterSchema()
            data = schema.load(request.json)
            
            # Check if user already exists
            existing_user = User.find_by_email(data['email'])
            if existing_user:
                return jsonify({
                    'success': False,
                    'error': 'User already exists with this email',
                    'status': 409
                }), 409
            
            # Validate password strength
            is_valid, message = validate_password_strength(data['password'])
            if not is_valid:
                return jsonify({
                    'success': False,
                    'error': message,
                    'status': 400
                }), 400
            
            # Hash password
            hashed_password = hash_password(data['password'])
            
            # Create user object
            user = User(
                email=data['email'],
                password=hashed_password,
                full_name=data['full_name'],
                preferences=data.get('preferences', {})
            )
            
            # Generate avatar initials
            name_parts = user.full_name.split()
            user.avatar_initials = ''.join([part[:1] for part in name_parts[:2]]).upper()
            
            # Create user in database
            user_id = user.create()
            
            # Generate tokens
            access_token = generate_access_token(user_id)
            refresh_token = generate_refresh_token(user_id)
            
            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'data': {
                    'user_id': user_id,
                    'email': user.email,
                    'full_name': user.full_name,
                    'avatar_initials': user.avatar_initials,
                    'preferences': user.preferences
                },
                'tokens': {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'token_type': 'Bearer'
                }
            }), 201
            
        except ValidationError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'details': e.messages,
                'status': 400
            }), 400
        except Exception as e:
            current_app.logger.error(f"Registration error: {e}")
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'status': 500
            }), 500
    
    @staticmethod
    def login():
        """Login user and return tokens."""
        try:
            # Validate request data
            schema = UserLoginSchema()
            data = schema.load(request.json)
            
            # Find user
            user = User.find_by_email(data['email'])
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'Invalid email or password',
                    'status': 401
                }), 401
            
            # Verify password
            if not verify_password(data['password'], user.password):
                return jsonify({
                    'success': False,
                    'error': 'Invalid email or password',
                    'status': 401
                }), 401
            
            # Update last login and compute user id safely
            user_id = AuthController._get_user_id(user)
            if user_id is None:
                raise Exception('User object missing id')
            user.update_last_login(user_id)
            
            # Generate tokens
            access_token = generate_access_token(user_id)
            refresh_token = generate_refresh_token(user_id)
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'data': {
                    'user_id': user_id,
                    'email': user.email,
                    'full_name': user.full_name,
                    'avatar_initials': user.avatar_initials,
                    'role': user.role,
                    'preferences': user.preferences,
                    'last_login': user.last_login
                },
                'tokens': {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'token_type': 'Bearer'
                }
            }), 200
            
        except ValidationError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'details': e.messages,
                'status': 400
            }), 400
        except Exception as e:
            current_app.logger.error(f"Login error: {e}")
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'status': 500
            }), 500
    
    @staticmethod
    def refresh_token():
        """Refresh access token using refresh token."""
        try:
            # Get refresh token from request
            if not request.json or 'refresh_token' not in request.json:
                return jsonify({
                    'success': False,
                    'error': 'Refresh token required',
                    'status': 400
                }), 400
            
            refresh_token = request.json['refresh_token']
            
            # Decode refresh token
            payload = decode_token(refresh_token, 'refresh')
            if not payload:
                return jsonify({
                    'success': False,
                    'error': 'Invalid or expired refresh token',
                    'status': 401
                }), 401
            
            # Verify user still exists
            user = User.find_by_id(payload['user_id'])
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'User not found',
                    'status': 401
                }), 401
            # Generate new access token (compute id safely)
            user_id = AuthController._get_user_id(user)
            if user_id is None:
                raise Exception('User object missing id')
            access_token = generate_access_token(user_id)
            
            return jsonify({
                'success': True,
                'message': 'Token refreshed successfully',
                'tokens': {
                    'access_token': access_token,
                    'refresh_token': refresh_token,  # Keep existing refresh token
                    'token_type': 'Bearer'
                }
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Token refresh error: {e}")
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'status': 500
            }), 500
    
    @staticmethod
    def get_current_user():
        """Get current user profile."""
        try:
            if not hasattr(request, 'user'):
                return jsonify({
                    'success': False,
                    'error': 'Authentication required',
                    'status': 401
                }), 401
            
            user = request.user
            user_id = AuthController._get_user_id(user)
            if user_id is None:
                return jsonify({
                    'success': False,
                    'error': 'User object missing id',
                    'status': 500
                }), 500
            
            return jsonify({
                'success': True,
                'data': {
                    'user_id': user_id,
                    'email': user.email,
                    'full_name': user.full_name,
                    'role': user.role,
                    'avatar_initials': user.avatar_initials,
                    'preferences': user.preferences,
                    'created_at': user.created_at,
                    'updated_at': user.updated_at,
                    'last_login': user.last_login
                }
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Get user error: {e}")
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'status': 500
            }), 500
    
    @staticmethod
    def update_profile():
        """Update current user profile."""
        try:
            if not hasattr(request, 'user'):
                return jsonify({
                    'success': False,
                    'error': 'Authentication required',
                    'status': 401
                }), 401
            
            # Validate request data
            schema = UserUpdateSchema()
            data = schema.load(request.json)
            
            user = request.user
            user_id = AuthController._get_user_id(user)
            if user_id is None:
                return jsonify({
                    'success': False,
                    'error': 'User object missing id',
                    'status': 500
                }), 500
            
            # Update user
            user.update(user_id, data)
            
            # Get updated user
            updated_user = User.find_by_id(user_id)
            
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully',
                'data': {
                    'user_id': user_id,
                    'email': updated_user.email,
                    'full_name': updated_user.full_name,
                    'avatar_initials': updated_user.avatar_initials,
                    'preferences': updated_user.preferences,
                    'updated_at': updated_user.updated_at
                }
            }), 200
            
        except ValidationError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'details': e.messages,
                'status': 400
            }), 400
        except Exception as e:
            current_app.logger.error(f"Update profile error: {e}")
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'status': 500
            }), 500
    
    @staticmethod
    def change_password():
        """Change user password."""
        try:
            if not hasattr(request, 'user'):
                return jsonify({
                    'success': False,
                    'error': 'Authentication required',
                    'status': 401
                }), 401
            
            # Validate request data
            schema = PasswordChangeSchema()
            data = schema.load(request.json)
            
            user = request.user
            
            # Verify current password
            if not verify_password(data['current_password'], user.password):
                return jsonify({
                    'success': False,
                    'error': 'Current password is incorrect',
                    'status': 400
                }), 400
            
            # Validate new password strength
            is_valid, message = validate_password_strength(data['new_password'])
            if not is_valid:
                return jsonify({
                    'success': False,
                    'error': message,
                    'status': 400
                }), 400
            
            # Hash new password
            new_hashed_password = hash_password(data['new_password'])
            
            # Update password
            user_id = AuthController._get_user_id(user)
            if user_id is None:
                return jsonify({
                    'success': False,
                    'error': 'User object missing id',
                    'status': 500
                }), 500
            user.update(user_id, {'password': new_hashed_password})
            
            return jsonify({
                'success': True,
                'message': 'Password changed successfully'
            }), 200
            
        except ValidationError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'details': e.messages,
                'status': 400
            }), 400
        except Exception as e:
            current_app.logger.error(f"Change password error: {e}")
            return jsonify({
                'success': False,
                'error': 'Internal server error',
                'status': 500
            }), 500
    
    @staticmethod
    def logout():
        """Logout user (client-side token invalidation)."""
        return jsonify({
            'success': True,
            'message': 'Logout successful'
        }), 200
