"""
Notification controller for managing user notifications
"""

from flask import jsonify, current_app, request
from ..models.notification import Notification
from ..middleware.auth_middleware import get_current_user_id

class NotificationController:
    """Notification controller for notification management."""
    
    @staticmethod
    def get_all_notifications():
        """Get all notifications for the current user."""
        try:
            user_id = get_current_user_id()
            
            # Get query parameters
            unread_only = request.args.get('unread_only', 'false').lower() == 'true'
            
            # Change to use read parameter instead of unread_only
            read_filter = False if unread_only else None
            notifications = Notification.find_by_user(user_id, read=read_filter)
            
            notifications_data = []
            for notification in notifications:
                notif_dict = notification.to_dict()
                # Handle potential missing _id
                if '_id' in notif_dict:
                    notif_dict['id'] = str(notif_dict.pop('_id'))
                notifications_data.append(notif_dict)
            
            return jsonify({
                'success': True,
                'data': notifications_data,
                'count': len(notifications_data)
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Get notifications error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to fetch notifications'
            }), 500
    
    @staticmethod
    def mark_as_read(notification_id):
        """Mark a notification as read."""
        try:
            user_id = get_current_user_id()
            
            notification = Notification(user_id=user_id, notification_type='info', title='', description='')
            updated = notification.mark_as_read(notification_id, user_id)
            
            if not updated:
                return jsonify({
                    'success': False,
                    'error': 'Notification not found'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Notification marked as read'
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Mark notification error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to mark notification as read'
            }), 500
    
    @staticmethod
    def mark_all_as_read():
        """Mark all notifications as read."""
        try:
            user_id = get_current_user_id()
            
            notification = Notification(user_id=user_id, notification_type='info', title='', description='')
            notification.mark_all_as_read(user_id)
            
            return jsonify({
                'success': True,
                'message': 'All notifications marked as read'
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Mark all notifications error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to mark all notifications as read'
            }), 500
    
    @staticmethod
    def delete_notification(notification_id):
        """Delete a notification."""
        try:
            user_id = get_current_user_id()
            
            notification = Notification(user_id=user_id, notification_type='info', title='', description='')
            deleted = notification.delete(notification_id, user_id)
            
            if not deleted:
                return jsonify({
                    'success': False,
                    'error': 'Notification not found'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Notification deleted successfully'
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Delete notification error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to delete notification'
            }), 500
