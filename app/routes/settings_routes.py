"""
Settings routes using Flask Blueprints
"""

from flask import Blueprint
from ..controllers.settings_controller import SettingsController
from ..middleware.auth_middleware import require_auth

settings_bp = Blueprint('settings', __name__)

# Settings endpoints
settings_bp.route('', methods=['GET'])(require_auth(SettingsController.get_settings))
settings_bp.route('', methods=['PUT'])(require_auth(SettingsController.update_settings))
