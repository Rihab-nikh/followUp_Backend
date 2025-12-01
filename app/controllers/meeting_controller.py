"""
Meeting controller for CRUD operations
"""

from flask import jsonify, current_app, request
from marshmallow import ValidationError
from ..models.meeting import Meeting
from ..schemas.meeting_schema import MeetingCreateSchema, MeetingUpdateSchema
from ..middleware.auth_middleware import get_current_user_id
from bson import ObjectId

class MeetingController:
    """Meeting controller for business meeting management."""
    
    @staticmethod
    def get_all_meetings():
        """Get all meetings for the current user."""
        try:
            user_id = get_current_user_id()
            
            # Get query parameters for filtering
            status = request.args.get('status')
            date_from = request.args.get('date_from')
            date_to = request.args.get('date_to')
            
            meetings = Meeting.find_by_user(user_id, status, date_from, date_to)
            
            meetings_data = []
            for meeting in meetings:
                meeting_dict = meeting.to_dict()
                meeting_dict['id'] = str(meeting_dict.pop('_id', ''))
                meetings_data.append(meeting_dict)
            
            return jsonify({
                'success': True,
                'data': meetings_data,
                'count': len(meetings_data)
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Get meetings error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to fetch meetings'
            }), 500
    
    @staticmethod
    def get_meeting(meeting_id):
        """Get a specific meeting by ID."""
        try:
            user_id = get_current_user_id()
            
            meeting = Meeting.find_by_id(meeting_id, user_id)
            
            if not meeting:
                return jsonify({
                    'success': False,
                    'error': 'Meeting not found'
                }), 404
            
            meeting_dict = meeting.to_dict()
            meeting_dict['id'] = meeting_id
            
            return jsonify({
                'success': True,
                'data': meeting_dict
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Get meeting error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to fetch meeting'
            }), 500
    
    @staticmethod
    def create_meeting():
        """Create a new meeting."""
        try:
            user_id = get_current_user_id()
            
            schema = MeetingCreateSchema()
            data = schema.load(request.json)
            
            meeting = Meeting(
                user_id=user_id,
                **data
            )
            
            meeting_id = meeting.create()
            
            return jsonify({
                'success': True,
                'message': 'Meeting created successfully',
                'data': {
                    'id': meeting_id
                }
            }), 201
            
        except ValidationError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'details': e.messages
            }), 400
        except Exception as e:
            current_app.logger.error(f"Create meeting error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to create meeting'
            }), 500
    
    @staticmethod
    def update_meeting(meeting_id):
        """Update an existing meeting."""
        try:
            user_id = get_current_user_id()
            
            schema = MeetingUpdateSchema()
            data = schema.load(request.json)
            
            meeting = Meeting(user_id=user_id, company='', contact='', subject='', date='', time='')
            updated = meeting.update(meeting_id, user_id, data)
            
            if not updated:
                return jsonify({
                    'success': False,
                    'error': 'Meeting not found or not updated'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Meeting updated successfully'
            }), 200
            
        except ValidationError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'details': e.messages
            }), 400
        except Exception as e:
            current_app.logger.error(f"Update meeting error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to update meeting'
            }), 500
    
    @staticmethod
    def delete_meeting(meeting_id):
        """Delete a meeting."""
        try:
            user_id = get_current_user_id()
            
            meeting = Meeting(user_id=user_id, company='', contact='', subject='', date='', time='')
            deleted = meeting.delete(meeting_id, user_id)
            
            if not deleted:
                return jsonify({
                    'success': False,
                    'error': 'Meeting not found or already deleted'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Meeting deleted successfully'
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Delete meeting error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to delete meeting'
            }), 500
