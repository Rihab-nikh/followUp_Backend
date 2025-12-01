"""
Settings controller for user preferences and configuration
"""

from flask import jsonify, current_app, request
from ..models.user import User
from ..middleware.auth_middleware import get_current_user_id
from marshmallow import ValidationError

class SettingsController:
    """Settings controller for user preferences."""
    
    @staticmethod
    def get_settings():
        """Get user settings and preferences."""
        try:
            user_id = get_current_user_id()
            
            user = User.find_by_id(user_id)
            
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'User not found'
                }), 404
            
            user_dict = user.to_dict()
            
            settings = {
                'email': user_dict.get('email'),
                'full_name': user_dict.get('full_name'),
                'avatar_initials': user_dict.get('avatar_initials'),
                'preferences': user_dict.get('preferences', {})
            }
            
            return jsonify({
                'success': True,
                'data': settings
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Get settings error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to fetch settings'
            }), 500
    
    @staticmethod
    def update_settings():
        """Update user settings and preferences."""
        try:
            user_id = get_current_user_id()
            
            data = request.json
            
            # Extract updatable fields
            update_data = {}
            if 'full_name' in data:
                update_data['full_name'] = data['full_name']
                # Update avatar initials based on new name
                name_parts = data['full_name'].split()
                update_data['avatar_initials'] = ''.join([part[:1] for part in name_parts[:2]]).upper()
            
            if 'preferences' in data:
                update_data['preferences'] = data['preferences']
            
            user = User(email='', password='', full_name='')
            updated = user.update(user_id, update_data)
            
            if not updated:
                return jsonify({
                    'success': False,
                    'error': 'Failed to update settings'
                }), 400
            
            return jsonify({
                'success': True,
                'message': 'Settings updated successfully'
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Update settings error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to update settings'
            }), 500
