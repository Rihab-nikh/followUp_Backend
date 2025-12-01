"""
Dashboard and KPI validation schemas using Marshmallow
"""

from marshmallow import Schema, fields, validate
from datetime import datetime

class KPIMetricSchema(Schema):
    """KPI metric validation schema."""
    id = fields.Str(dump_only=True)
    user_id = fields.Str(required=True)
    date = fields.Str(required=True, validate=validate.Regexp(r'^\d{4}-\d{2}-\d{2}$'))
    meetings_scheduled = fields.Int(missing=0, validate=validate.Range(min=0))
    meetings_completed = fields.Int(missing=0, validate=validate.Range(min=0))
    tasks_completed = fields.Int(missing=0, validate=validate.Range(min=0))
    tasks_pending = fields.Int(missing=0, validate=validate.Range(min=0))
    follow_ups_required = fields.Int(missing=0, validate=validate.Range(min=0))
    created_at = fields.DateTime(dump_only=True)

class DashboardKPIsSchema(Schema):
    """Dashboard KPIs response schema."""
    upcoming_meetings = fields.Int()
    completed_tasks = fields.Int()
    clients_to_follow_up = fields.Int()
    overall_progress = fields.Int(validate=validate.Range(min=0, max=100))

class ChartDataPointSchema(Schema):
    """Chart data point validation schema."""
    name = fields.Str(required=True)
    meetings = fields.Int(validate=validate.Range(min=0))

class MeetingActivityChartSchema(Schema):
    """Meeting activity chart response schema."""
    data = fields.List(fields.Nested(ChartDataPointSchema))

class RecentItemSchema(Schema):
    """Recent item (meeting or task) schema."""
    id = fields.Str()
    title = fields.Str()
    subtitle = fields.Str()
    time = fields.Str()
    status = fields.Str()
    priority = fields.Str()
    avatar = fields.Str()

class RecentMeetingsSchema(Schema):
    """Recent meetings response schema."""
    meetings = fields.List(fields.Nested(RecentItemSchema))

class UpcomingTasksSchema(Schema):
    """Upcoming tasks response schema."""
    tasks = fields.List(fields.Nested(RecentItemSchema))

class DashboardAnalyticsSchema(Schema):
    """Complete dashboard analytics response schema."""
    kpis = fields.Nested(DashboardKPIsSchema)
    chart_data = fields.Nested(MeetingActivityChartSchema)
    recent_meetings = fields.Nested(RecentMeetingsSchema)
    upcoming_tasks = fields.Nested(UpcomingTasksSchema)

class DateRangeSchema(Schema):
    """Date range validation schema."""
    start_date = fields.Str(validate=validate.Regexp(r'^\d{4}-\d{2}-\d{2}$'))
    end_date = fields.Str(validate=validate.Regexp(r'^\d{4}-\d{2}-\d{2}$'))
