"""
Notification routes using Flask Blueprints
"""

from flask import Blueprint
from ..controllers.notification_controller import NotificationController
from ..middleware.auth_middleware import require_auth

notification_bp = Blueprint('notifications', __name__)

# Notification endpoints
notification_bp.route('', methods=['GET'])(require_auth(NotificationController.get_all_notifications))
notification_bp.route('/<notification_id>/read', methods=['PUT'])(require_auth(NotificationController.mark_as_read))
notification_bp.route('/read-all', methods=['PUT'])(require_auth(NotificationController.mark_all_as_read))
notification_bp.route('/<notification_id>', methods=['DELETE'])(require_auth(NotificationController.delete_notification))
