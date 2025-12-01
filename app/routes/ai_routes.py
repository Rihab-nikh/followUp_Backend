"""
AI routes using Flask Blueprints
"""

from flask import Blueprint
from ..controllers.ai_controller import AIController
from ..middleware.auth_middleware import require_auth

ai_bp = Blueprint('ai', __name__)

# AI endpoints
ai_bp.route('/chat', methods=['POST'])(require_auth(AIController.chat))
ai_bp.route('/chat/history', methods=['GET'])(require_auth(AIController.get_chat_history))
