"""
Notification model for MongoDB
"""

from datetime import datetime
from bson import ObjectId
from ..utils.db import get_collection

def create_notification_indexes():
    """Create indexes for notifications collection."""
    notifications = get_collection('notifications')
    notifications.create_index('user_id')
    notifications.create_index('created_at')
    notifications.create_index('read')
    return True

class Notification:
    """Notification model for user notifications."""
    
    def __init__(self, user_id, notification_type, title, description, 
                 read=False, meeting_id=None, task_id=None, _id=None, created_at=None):
        # Preserve DB id if provided
        self._id = _id
        try:
            self.id = str(_id) if _id is not None else None
        except Exception:
            self.id = None

        self.user_id = user_id
        self.type = notification_type  # meeting, task, followup, system
        self.title = title
        self.description = description
        self.read = read
        self.meeting_id = meeting_id
        self.task_id = task_id
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self):
        """Convert notification object to dictionary."""
        return {
            'user_id': self.user_id,
            'type': self.type,
            'title': self.title,
            'description': self.description,
            'read': self.read,
            'meeting_id': self.meeting_id,
            'task_id': self.task_id,
            'created_at': self.created_at
        }
    
    @classmethod
    def find_by_user(cls, user_id, read=None, limit=50, skip=0):
        """Find notifications by user with optional filter for read status."""
        collection = get_collection('notifications')
        query = {'user_id': user_id}
        
        if read is not None:
            query['read'] = read
        
        cursor = collection.find(query).sort('created_at', -1).skip(skip).limit(limit)
        return [cls(**notification_data) for notification_data in cursor]
    
    @classmethod
    def find_by_id(cls, notification_id, user_id=None):
        """Find notification by ID, optionally filtered by user."""
        collection = get_collection('notifications')
        query = {'_id': ObjectId(notification_id) if isinstance(notification_id, str) else notification_id}
        if user_id:
            query['user_id'] = user_id
        
        notification_data = collection.find_one(query)
        return cls(**notification_data) if notification_data else None
    
    @classmethod
    def count_unread(cls, user_id):
        """Count unread notifications for user."""
        collection = get_collection('notifications')
        count = collection.count_documents({
            'user_id': user_id,
            'read': False
        })
        return count
    
    @classmethod
    def find_by_type(cls, user_id, notification_type):
        """Find notifications by type."""
        collection = get_collection('notifications')
        query = {
            'user_id': user_id,
            'type': notification_type
        }
        cursor = collection.find(query).sort('created_at', -1)
        return [cls(**notification_data) for notification_data in cursor]
    
    @classmethod
    def find_recent(cls, user_id, hours=24):
        """Find notifications from last N hours."""
        collection = get_collection('notifications')
        from datetime import datetime, timedelta
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        query = {
            'user_id': user_id,
            'created_at': {'$gte': cutoff_time}
        }
        
        cursor = collection.find(query).sort('created_at', -1)
        return [cls(**notification_data) for notification_data in cursor]
    
    def create(self):
        """Create notification in database."""
        collection = get_collection('notifications')
        notification_data = self.to_dict()
        result = collection.insert_one(notification_data)
        return str(result.inserted_id)
    
    def mark_as_read(self, notification_id, user_id):
        """Mark notification as read."""
        collection = get_collection('notifications')
        notification_id = ObjectId(notification_id) if isinstance(notification_id, str) else notification_id
        
        result = collection.update_one(
            {'_id': notification_id, 'user_id': user_id}, 
            {'$set': {'read': True}}
        )
        return result.modified_count > 0
    
    def mark_all_as_read(self, user_id):
        """Mark all notifications as read for user."""
        collection = get_collection('notifications')
        result = collection.update_many(
            {'user_id': user_id, 'read': False}, 
            {'$set': {'read': True}}
        )
        return result.modified_count > 0
    
    def delete(self, notification_id, user_id):
        """Delete notification."""
        collection = get_collection('notifications')
        notification_id = ObjectId(notification_id) if isinstance(notification_id, str) else notification_id
        
        result = collection.delete_one({
            '_id': notification_id, 
            'user_id': user_id
        })
        return result.deleted_count > 0
    
    def delete_all_read(self, user_id):
        """Delete all read notifications for user."""
        collection = get_collection('notifications')
        result = collection.delete_many({
            'user_id': user_id,
            'read': True
        })
        return result.deleted_count > 0
    
    @classmethod
    def create_meeting_notification(cls, user_id, meeting, action='reminder'):
        """Create notification for meeting events."""
        if action == 'reminder':
            return cls(
                user_id=user_id,
                notification_type='meeting',
                title=f'Upcoming Meeting: {meeting.company}',
                description=f'{meeting.subject} at {meeting.time} with {meeting.contact}',
                meeting_id=str(meeting.id) if hasattr(meeting, 'id') else None
            )
        elif action == 'created':
            return cls(
                user_id=user_id,
                notification_type='meeting',
                title=f'Meeting Scheduled: {meeting.company}',
                description=f'{meeting.subject} scheduled for {meeting.date} at {meeting.time}',
                meeting_id=str(meeting.id) if hasattr(meeting, 'id') else None
            )
        elif action == 'completed':
            return cls(
                user_id=user_id,
                notification_type='meeting',
                title=f'Meeting Completed: {meeting.company}',
                description=f'{meeting.subject} has been completed',
                meeting_id=str(meeting.id) if hasattr(meeting, 'id') else None
            )
        elif action == 'cancelled':
            return cls(
                user_id=user_id,
                notification_type='meeting',
                title=f'Meeting Cancelled: {meeting.company}',
                description=f'{meeting.subject} has been cancelled',
                meeting_id=str(meeting.id) if hasattr(meeting, 'id') else None
            )
    
    @classmethod
    def create_task_notification(cls, user_id, task, action='created'):
        """Create notification for task events."""
        if action == 'created':
            return cls(
                user_id=user_id,
                notification_type='task',
                title=f'New Task Assigned: {task.title}',
                description=f'Task assigned to {task.assignee} due {task.due_date}',
                task_id=str(task.id) if hasattr(task, 'id') else None
            )
        elif action == 'due_today':
            return cls(
                user_id=user_id,
                notification_type='task',
                title=f'Task Due Today: {task.title}',
                description=f'Remember to complete "{task.title}" today',
                task_id=str(task.id) if hasattr(task, 'id') else None
            )
        elif action == 'overdue':
            return cls(
                user_id=user_id,
                notification_type='task',
                title=f'Task Overdue: {task.title}',
                description=f'"{task.title}" was due {task.due_date}',
                task_id=str(task.id) if hasattr(task, 'id') else None
            )
        elif action == 'completed':
            return cls(
                user_id=user_id,
                notification_type='task',
                title=f'Task Completed: {task.title}',
                description=f'"{task.title}" has been marked as completed',
                task_id=str(task.id) if hasattr(task, 'id') else None
            )
