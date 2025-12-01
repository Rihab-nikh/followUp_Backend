"""
Task controller for CRUD operations
"""

from flask import jsonify, current_app, request
from marshmallow import ValidationError
from ..models.task import Task
from ..schemas.task_schema import TaskCreateSchema, TaskUpdateSchema
from ..middleware.auth_middleware import get_current_user_id

class TaskController:
    """Task controller for task management."""
    
    @staticmethod
    def get_all_tasks():
        """Get all tasks for the current user."""
        try:
            user_id = get_current_user_id()
            
            # Get query parameters for filtering
            status = request.args.get('status')
            priority = request.args.get('priority')
            assignee = request.args.get('assignee')
            
            tasks = Task.find_by_user(user_id, status, priority, assignee)
            
            tasks_data = []
            for task in tasks:
                task_dict = task.to_dict()
                task_dict['id'] = str(task_dict.pop('_id', ''))
                # Convert dueDate to due_date for frontend compatibility
                if 'due_date' in task_dict:
                    task_dict['dueDate'] = task_dict['due_date']
                tasks_data.append(task_dict)
            
            return jsonify({
                'success': True,
                'data': tasks_data,
                'count': len(tasks_data)
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Get tasks error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to fetch tasks'
            }), 500
    
    @staticmethod
    def get_task(task_id):
        """Get a specific task by ID."""
        try:
            user_id = get_current_user_id()
            
            task = Task.find_by_id(task_id, user_id)
            
            if not task:
                return jsonify({
                    'success': False,
                    'error': 'Task not found'
                }), 404
            
            task_dict = task.to_dict()
            task_dict['id'] = task_id
            
            return jsonify({
                'success': True,
                'data': task_dict
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Get task error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to fetch task'
            }), 500
    
    @staticmethod
    def create_task():
        """Create a new task."""
        try:
            user_id = get_current_user_id()
            
            schema = TaskCreateSchema()
            data = schema.load(request.json)
            
            task = Task(
                user_id=user_id,
                **data
            )
            
            task_id = task.create()
            
            return jsonify({
                'success': True,
                'message': 'Task created successfully',
                'data': {
                    'id': task_id
                }
            }), 201
            
        except ValidationError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'details': e.messages
            }), 400
        except Exception as e:
            current_app.logger.error(f"Create task error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to create task'
            }), 500
    
    @staticmethod
    def update_task(task_id):
        """Update an existing task."""
        try:
            user_id = get_current_user_id()
            
            schema = TaskUpdateSchema()
            data = schema.load(request.json)
            
            task = Task(user_id=user_id, title='')
            updated = task.update(task_id, user_id, data)
            
            if not updated:
                return jsonify({
                    'success': False,
                    'error': 'Task not found or not updated'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Task updated successfully'
            }), 200
            
        except ValidationError as e:
            return jsonify({
                'success': False,
                'error': 'Validation error',
                'details': e.messages
            }), 400
        except Exception as e:
            current_app.logger.error(f"Update task error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to update task'
            }), 500
    
    @staticmethod
    def delete_task(task_id):
        """Delete a task."""
        try:
            user_id = get_current_user_id()
            
            task = Task(user_id=user_id, title='')
            deleted = task.delete(task_id, user_id)
            
            if not deleted:
                return jsonify({
                    'success': False,
                    'error': 'Task not found or already deleted'
                }), 404
            
            return jsonify({
                'success': True,
                'message': 'Task deleted successfully'
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Delete task error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to delete task'
            }), 500
