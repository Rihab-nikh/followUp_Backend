"""
Task model for MongoDB
"""

from datetime import datetime
from bson import ObjectId
from ..utils.db import get_collection

def create_task_indexes():
    """Create indexes for tasks collection."""
    tasks = get_collection('tasks')
    tasks.create_index('user_id')
    tasks.create_index('due_date')
    tasks.create_index('status')
    tasks.create_index('assignee')
    return True

class Task:
    """Task model for task management and Kanban boards."""
    
    def __init__(self, user_id, title, description=None, meeting_id=None, 
                 assignee=None, assignee_user_id=None, due_date=None, 
                 priority='medium', status='todo', tags=None,
                 _id=None, created_at=None, updated_at=None, completed_at=None):
        # Preserve DB id if provided
        self._id = _id
        try:
            self.id = str(_id) if _id is not None else None
        except Exception:
            self.id = None

        self.user_id = user_id
        self.title = title
        self.description = description
        self.meeting_id = meeting_id
        self.assignee = assignee
        self.assignee_user_id = assignee_user_id
        self.due_date = due_date  # Format: YYYY-MM-DD
        self.priority = priority  # high, medium, low
        self.status = status  # todo, inprogress, done
        self.tags = tags or []
        # Preserve timestamps if provided (e.g., when loading from DB)
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.completed_at = completed_at
    
    def to_dict(self):
        """Convert task object to dictionary."""
        return {
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'meeting_id': self.meeting_id,
            'assignee': self.assignee,
            'assignee_user_id': self.assignee_user_id,
            'due_date': self.due_date,
            'priority': self.priority,
            'status': self.status,
            'tags': self.tags,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'completed_at': self.completed_at
        }
    
    @classmethod
    def find_by_user(cls, user_id, status=None, priority=None, assignee=None):
        """Find tasks by user with optional filters."""
        collection = get_collection('tasks')
        query = {'user_id': user_id}
        
        if status:
            query['status'] = status
        
        if priority:
            query['priority'] = priority
        
        if assignee:
            query['assignee'] = assignee
        
        cursor = collection.find(query).sort('due_date', 1)
        return [cls(**task_data) for task_data in cursor]
    
    @classmethod
    def find_by_id(cls, task_id, user_id=None):
        """Find task by ID, optionally filtered by user."""
        collection = get_collection('tasks')
        query = {'_id': ObjectId(task_id) if isinstance(task_id, str) else task_id}
        if user_id:
            query['user_id'] = user_id
        
        task_data = collection.find_one(query)
        return cls(**task_data) if task_data else None
    
    @classmethod
    def find_by_meeting(cls, meeting_id, user_id):
        """Find tasks associated with a specific meeting."""
        collection = get_collection('tasks')
        query = {
            'user_id': user_id,
            'meeting_id': meeting_id
        }
        cursor = collection.find(query).sort('priority', -1)
        return [cls(**task_data) for task_data in cursor]
    
    @classmethod
    def find_upcoming(cls, user_id, days=7):
        """Find upcoming tasks within specified days."""
        collection = get_collection('tasks')
        from datetime import datetime, timedelta
        
        end_date = datetime.now() + timedelta(days=days)
        end_date_str = end_date.strftime('%Y-%m-%d')
        
        query = {
            'user_id': user_id,
            'due_date': {'$lte': end_date_str},
            'status': {'$ne': 'done'}
        }
        
        cursor = collection.find(query).sort('due_date', 1)
        return [cls(**task_data) for task_data in cursor]
    
    @classmethod
    def find_today(cls, user_id):
        """Find tasks due today."""
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        
        collection = get_collection('tasks')
        query = {
            'user_id': user_id,
            'due_date': today,
            'status': {'$ne': 'done'}
        }
        
        cursor = collection.find(query).sort('priority', -1)
        return [cls(**task_data) for task_data in cursor]
    
    @classmethod
    def find_overdue(cls, user_id):
        """Find overdue tasks."""
        from datetime import datetime
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        collection = get_collection('tasks')
        query = {
            'user_id': user_id,
            'due_date': {'$lt': today},
            'status': {'$ne': 'done'}
        }
        
        cursor = collection.find(query).sort('due_date', 1)
        return [cls(**task_data) for task_data in cursor]
    
    @classmethod
    def find_by_status(cls, user_id):
        """Find tasks grouped by status for Kanban board."""
        collection = get_collection('tasks')
        query = {'user_id': user_id}
        
        pipeline = [
            {'$match': query},
            {'$group': {
                '_id': '$status',
                'tasks': {'$push': {
                    'id': '$_id',
                    'title': '$title',
                    'description': '$description',
                    'due_date': '$due_date',
                    'priority': '$priority',
                    'assignee': '$assignee',
                    'tags': '$tags'
                }},
                'count': {'$sum': 1}
            }},
            {'$sort': {'_id': 1}}
        ]
        
        return list(collection.aggregate(pipeline))
    
    def create(self):
        """Create task in database."""
        collection = get_collection('tasks')
        task_data = self.to_dict()
        result = collection.insert_one(task_data)
        return str(result.inserted_id)
    
    def update(self, task_id, user_id, update_data):
        """Update task data."""
        collection = get_collection('tasks')
        task_id = ObjectId(task_id) if isinstance(task_id, str) else task_id
        
        # Handle status change and completed_at timestamp
        if 'status' in update_data:
            if update_data['status'] == 'done' and not self.completed_at:
                update_data['completed_at'] = datetime.utcnow()
            elif update_data['status'] != 'done':
                update_data['completed_at'] = None
        
        update_data['updated_at'] = datetime.utcnow()
        
        result = collection.update_one(
            {'_id': task_id, 'user_id': user_id}, 
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    def move_to_status(self, task_id, user_id, new_status):
        """Move task to a different status column."""
        collection = get_collection('tasks')
        task_id = ObjectId(task_id) if isinstance(task_id, str) else task_id
        
        update_data = {
            'status': new_status,
            'updated_at': datetime.utcnow()
        }
        
        # Set completed_at if moving to done
        if new_status == 'done':
            update_data['completed_at'] = datetime.utcnow()
        else:
            update_data['completed_at'] = None
        
        result = collection.update_one(
            {'_id': task_id, 'user_id': user_id}, 
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    def delete(self, task_id, user_id):
        """Delete task."""
        collection = get_collection('tasks')
        task_id = ObjectId(task_id) if isinstance(task_id, str) else task_id
        
        result = collection.delete_one({
            '_id': task_id, 
            'user_id': user_id
        })
        return result.deleted_count > 0
