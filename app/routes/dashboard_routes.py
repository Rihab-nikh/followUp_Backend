"""
Dashboard routes using Flask Blueprints
"""

from flask import Blueprint
from ..controllers.dashboard_controller import DashboardController
from ..middleware.auth_middleware import require_auth

dashboard_bp = Blueprint('dashboard', __name__)

# Dashboard endpoints
dashboard_bp.route('/kpis', methods=['GET'])(require_auth(DashboardController.get_dashboard_kpis))
dashboard_bp.route('/activity', methods=['GET'])(require_auth(DashboardController.get_recent_activity))
