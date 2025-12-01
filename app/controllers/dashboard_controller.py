"""
Dashboard controller for KPIs and analytics
"""

from flask import jsonify, current_app
from ..models.meeting import Meeting
from ..models.task import Task
from ..models.notification import Notification
from ..middleware.auth_middleware import get_current_user_id
from datetime import datetime, timedelta

class DashboardController:
    """Dashboard controller for analytics and KPIs."""
    
    @staticmethod
    def get_dashboard_kpis():
        """Get dashboard KPIs for the current user."""
        try:
            user_id = get_current_user_id()
            
            # Calculate date ranges
            today = datetime.now()
            week_ago = today - timedelta(days=7)
            month_ago = today - timedelta(days=30)
            
            today_str = today.strftime('%Y-%m-%d')
            week_ago_str = week_ago.strftime('%Y-%m-%d')
            month_ago_str = month_ago.strftime('%Y-%m-%d')
            
            # Get meetings stats
            all_meetings = Meeting.find_by_user(user_id)
            today_meetings = Meeting.find_today(user_id)
            upcoming_meetings = Meeting.find_upcoming(user_id, days=7)
            completed_meetings = Meeting.find_by_user(user_id, status='completed')
            
            # Get task stats
            all_tasks = Task.find_by_user(user_id)
            todo_tasks = Task.find_by_user(user_id, status='todo')
            inprogress_tasks = Task.find_by_user(user_id, status='inprogress')
            done_tasks = Task.find_by_user(user_id, status='done')
            overdue_tasks = Task.find_overdue(user_id)
            
            # Get notification stats
            all_notifications = Notification.find_by_user(user_id, read=None)
            unread_notifications = Notification.find_by_user(user_id, read=False)
            
            # Calculate KPIs
            total_meetings = len(all_meetings)
            total_tasks = len(all_tasks)
            completion_rate = (len(done_tasks) / total_tasks * 100) if total_tasks > 0 else 0
            
            kpis = {
                'total_meetings': total_meetings,
                'today_meetings': len(today_meetings),
                'upcoming_meetings': len(upcoming_meetings),
                'completed_meetings': len(completed_meetings),
                'total_tasks': total_tasks,
                'todo_tasks': len(todo_tasks),
                'inprogress_tasks': len(inprogress_tasks),
                'done_tasks': len(done_tasks),
                'overdue_tasks': len(overdue_tasks),
                'task_completion_rate': round(completion_rate, 1),
                'total_notifications': len(all_notifications),
                'unread_notifications': len(unread_notifications)
            }
            
            return jsonify({
                'success': True,
                'data': kpis
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Get dashboard KPIs error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to fetch dashboard data'
            }), 500
    
    @staticmethod
    def get_recent_activity():
        """Get recent activity for the current user."""
        try:
            user_id = get_current_user_id()
            
            # Get recent meetings
            recent_meetings = Meeting.find_by_user(user_id)[:5]
            
            # Get recent tasks
            recent_tasks = Task.find_by_user(user_id)[:5]
            
            # Format activity data
            activities = []
            
            for meeting in recent_meetings:
                meeting_dict = meeting.to_dict()
                activities.append({
                    'type': 'meeting',
                    'id': str(meeting_dict.get('_id', '')),
                    'title': f"Meeting with {meeting_dict.get('contact', '')} - {meeting_dict.get('company', '')}",
                    'date': meeting_dict.get('date', ''),
                    'status': meeting_dict.get('status', '')
                })
            
            for task in recent_tasks:
                task_dict = task.to_dict()
                activities.append({
                    'type': 'task',
                    'id': str(task_dict.get('_id', '')),
                    'title': task_dict.get('title', ''),
                    'due_date': task_dict.get('due_date', ''),
                    'status': task_dict.get('status', ''),
                    'priority': task_dict.get('priority', '')
                })
            
            # Sort by date
            activities = sorted(activities, key=lambda x: x.get('date') or x.get('due_date', ''), reverse=True)[:10]
            
            return jsonify({
                'success': True,
                'data': activities
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Get recent activity error: {e}")
            return jsonify({
                'success': False,
                'error': 'Failed to fetch recent activity'
            }), 500
