"""
Task routes using Flask Blueprints
"""

from flask import Blueprint
from ..controllers.task_controller import TaskController
from ..middleware.auth_middleware import require_auth

task_bp = Blueprint('tasks', __name__)

# Task endpoints
task_bp.route('', methods=['GET'])(require_auth(TaskController.get_all_tasks))
task_bp.route('/<task_id>', methods=['GET'])(require_auth(TaskController.get_task))
task_bp.route('', methods=['POST'])(require_auth(TaskController.create_task))
task_bp.route('/<task_id>', methods=['PUT'])(require_auth(TaskController.update_task))
task_bp.route('/<task_id>', methods=['DELETE'])(require_auth(TaskController.delete_task))
