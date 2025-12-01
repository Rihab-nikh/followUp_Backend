"""
Meeting routes using Flask Blueprints
"""

from flask import Blueprint
from ..controllers.meeting_controller import MeetingController
from ..middleware.auth_middleware import require_auth

meeting_bp = Blueprint('meetings', __name__)

# Meeting endpoints
meeting_bp.route('', methods=['GET'])(require_auth(MeetingController.get_all_meetings))
meeting_bp.route('/<meeting_id>', methods=['GET'])(require_auth(MeetingController.get_meeting))
meeting_bp.route('', methods=['POST'])(require_auth(MeetingController.create_meeting))
meeting_bp.route('/<meeting_id>', methods=['PUT'])(require_auth(MeetingController.update_meeting))
meeting_bp.route('/<meeting_id>', methods=['DELETE'])(require_auth(MeetingController.delete_meeting))
