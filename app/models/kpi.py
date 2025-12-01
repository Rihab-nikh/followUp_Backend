"""
KPI Metrics model for MongoDB
"""

from datetime import datetime, timedelta
from bson import ObjectId
from ..utils.db import get_collection

def create_kpi_indexes():
    """Create indexes for kpi_metrics collection."""
    kpi_metrics = get_collection('kpi_metrics')
    kpi_metrics.create_index('user_id')
    kpi_metrics.create_index('date')
    return True

class KPIMetric:
    """KPI metric model for dashboard analytics."""
    
    def __init__(self, user_id, date=None, metrics=None, _id=None, created_at=None):
        # Preserve DB id if provided
        self._id = _id
        try:
            self.id = str(_id) if _id is not None else None
        except Exception:
            self.id = None

        self.user_id = user_id
        self.date = date or datetime.now().strftime('%Y-%m-%d')
        metrics = metrics or {}
        self.meetings_scheduled = metrics.get('meetings_scheduled', 0)
        self.meetings_completed = metrics.get('meetings_completed', 0)
        self.tasks_completed = metrics.get('tasks_completed', 0)
        self.tasks_pending = metrics.get('tasks_pending', 0)
        self.follow_ups_required = metrics.get('follow_ups_required', 0)
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self):
        """Convert KPI metric object to dictionary."""
        return {
            'user_id': self.user_id,
            'date': self.date,
            'meetings_scheduled': self.meetings_scheduled,
            'meetings_completed': self.meetings_completed,
            'tasks_completed': self.tasks_completed,
            'tasks_pending': self.tasks_pending,
            'follow_ups_required': self.follow_ups_required,
            'created_at': self.created_at
        }
    
    @classmethod
    def find_by_user(cls, user_id, date_from=None, date_to=None):
        """Find KPI metrics by user with optional date range."""
        collection = get_collection('kpi_metrics')
        query = {'user_id': user_id}
        
        if date_from and date_to:
            query['date'] = {'$gte': date_from, '$lte': date_to}
        elif date_from:
            query['date'] = {'$gte': date_from}
        elif date_to:
            query['date'] = {'$lte': date_to}
        
        cursor = collection.find(query).sort('date', -1)
        return [cls(**metric_data) for metric_data in cursor]
    
    @classmethod
    def find_by_date(cls, user_id, date):
        """Find KPI metrics for specific date."""
        collection = get_collection('kpi_metrics')
        query = {
            'user_id': user_id,
            'date': date
        }
        metric_data = collection.find_one(query)
        return cls(**metric_data) if metric_data else None
    
    @classmethod
    def calculate_daily_metrics(cls, user_id, date=None):
        """Calculate metrics for a specific date."""
        from .meeting import Meeting
        from .task import Task
        from .user import User
        
        date = date or datetime.now().strftime('%Y-%m-%d')
        
        # Count meetings
        meetings_scheduled = len([m for m in Meeting.find_by_date(user_id, date) if m.status == 'scheduled'])
        meetings_completed = len([m for m in Meeting.find_by_date(user_id, date) if m.status == 'completed'])
        
        # Count tasks
        today_tasks = Task.find_by_user(user_id)
        tasks_completed_today = len([t for t in today_tasks if t.completed_at and t.completed_at.strftime('%Y-%m-%d') == date])
        tasks_pending_today = len([t for t in today_tasks if t.status != 'done' and t.due_date == date])
        
        # Calculate follow-ups required
        follow_ups_required = 0
        completed_meetings = [m for m in Meeting.find_by_user(user_id) if m.status == 'completed']
        for meeting in completed_meetings:
            # Check if there are related tasks or if meeting was recent (within 3 days)
            if meeting.date >= (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'):
                related_tasks = Task.find_by_meeting(meeting.id, user_id) if hasattr(meeting, 'id') else []
                if not related_tasks or not any(t.status == 'done' for t in related_tasks):
                    follow_ups_required += 1
        
        metrics = {
            'meetings_scheduled': meetings_scheduled,
            'meetings_completed': meetings_completed,
            'tasks_completed': tasks_completed_today,
            'tasks_pending': tasks_pending_today,
            'follow_ups_required': follow_ups_required
        }
        
        return KPIMetric(user_id, date, metrics)
    
    def create(self):
        """Create KPI metric in database."""
        collection = get_collection('kpi_metrics')
        metric_data = self.to_dict()
        result = collection.insert_one(metric_data)
        return str(result.inserted_id)
    
    def update_or_create(self, user_id, date=None):
        """Update existing metric or create new one for specific date."""
        if not date:
            date = self.date
        
        collection = get_collection('kpi_metrics')
        
        # Check if metric exists for this date
        existing = collection.find_one({'user_id': user_id, 'date': date})
        
        if existing:
            # Update existing metric
            result = collection.update_one(
                {'_id': existing['_id']},
                {'$set': self.to_dict()}
            )
            return str(existing['_id']) if result.modified_count > 0 else None
        else:
            # Create new metric
            return self.create()
    
    @classmethod
    def get_chart_data(cls, user_id, days=7):
        """Get meeting activity chart data for last N days."""
        collection = get_collection('kpi_metrics')
        from datetime import datetime, timedelta
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days-1)
        
        start_date_str = start_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
        
        pipeline = [
            {
                '$match': {
                    'user_id': user_id,
                    'date': {'$gte': start_date_str, '$lte': end_date_str}
                }
            },
            {
                '$group': {
                    '_id': '$date',
                    'meetings_scheduled': {'$sum': '$meetings_scheduled'},
                    'meetings_completed': {'$sum': '$meetings_completed'}
                }
            },
            {
                '$sort': {'_id': 1}
            },
            {
                '$project': {
                    '_id': 0,
                    'date': '$_id',
                    'meetings': {'$add': ['$meetings_scheduled', '$meetings_completed']}
                }
            }
        ]
        
        result = list(collection.aggregate(pipeline))
        
        # Fill missing dates with 0 values
        chart_data = []
        for i in range(days):
            date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
            day_name = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][(start_date.weekday() + i) % 7]
            
            # Find existing data for this date
            day_data = next((d for d in result if d['date'] == date), None)
            
            chart_data.append({
                'name': day_name,
                'meetings': day_data['meetings'] if day_data else 0
            })
        
        return chart_data
    
    @classmethod
    def get_current_kpis(cls, user_id):
        """Get current KPI summary."""
        # Get latest metrics
        latest_metrics = cls.find_by_user(user_id, date_from=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        
        if not latest_metrics:
            # Calculate current metrics
            current_metrics = cls.calculate_daily_metrics(user_id)
            current_metrics.create()
            latest_metrics = [current_metrics]
        
        # Calculate totals
        total_meetings = sum(m.meetings_scheduled + m.meetings_completed for m in latest_metrics)
        total_completed_tasks = sum(m.tasks_completed for m in latest_metrics)
        current_follow_ups = latest_metrics[0].follow_ups_required if latest_metrics else 0
        
        # Calculate progress percentage
        total_pending = sum(m.tasks_pending for m in latest_metrics)
        progress_percentage = 0
        if total_completed_tasks > 0 or total_pending > 0:
            progress_percentage = round((total_completed_tasks / (total_completed_tasks + total_pending)) * 100)
        
        return {
            'upcoming_meetings': sum(m.meetings_scheduled for m in latest_metrics),
            'completed_tasks': total_completed_tasks,
            'clients_to_follow_up': current_follow_ups,
            'overall_progress': progress_percentage
        }
    
    @classmethod
    def auto_generate_metrics(cls, user_id):
        """Auto-generate missing metrics for recent dates."""
        from datetime import datetime, timedelta
        
        # Generate metrics for last 7 days
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            existing = cls.find_by_date(user_id, date)
            if not existing:
                metrics = cls.calculate_daily_metrics(user_id, date)
                metrics.create()
