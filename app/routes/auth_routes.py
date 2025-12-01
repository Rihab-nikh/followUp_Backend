"""
Authentication routes using Flask Blueprints
"""

from flask import Blueprint
from ..controllers.auth_controller import AuthController

auth_bp = Blueprint('auth', __name__)

# Authentication endpoints
auth_bp.route('/register', methods=['POST'])(AuthController.register)
auth_bp.route('/login', methods=['POST'])(AuthController.login)
auth_bp.route('/refresh', methods=['POST'])(AuthController.refresh_token)
auth_bp.route('/logout', methods=['POST'])(AuthController.logout)

# User profile endpoints
auth_bp.route('/me', methods=['GET'])(AuthController.get_current_user)
auth_bp.route('/me', methods=['PUT'])(AuthController.update_profile)
auth_bp.route('/password', methods=['PUT'])(AuthController.change_password)
