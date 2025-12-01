"""
Notification validation schemas using Marshmallow
"""

from marshmallow import Schema, fields, validate

class NotificationSchema(Schema):
    """Notification data validation schema."""
    id = fields.Str(dump_only=True)
    user_id = fields.Str(required=True)
    type = fields.Str(required=True, validate=validate.OneOf(['meeting', 'task', 'followup', 'system']))
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    read = fields.Bool(missing=False)
    meeting_id = fields.Str(missing=None)
    task_id = fields.Str(missing=None)
    created_at = fields.DateTime(dump_only=True)

class NotificationCreateSchema(Schema):
    """Notification creation validation schema."""
    type = fields.Str(required=True, validate=validate.OneOf(['meeting', 'task', 'followup', 'system']))
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    meeting_id = fields.Str(missing=None)
    task_id = fields.Str(missing=None)

class NotificationResponseSchema(Schema):
    """Notification response schema for API."""
    id = fields.Str()
    type = fields.Str()
    title = fields.Str()
    description = fields.Str()
    read = fields.Bool()
    meeting_id = fields.Str()
    task_id = fields.Str()
    created_at = fields.DateTime()

class NotificationUpdateSchema(Schema):
    """Notification update validation schema."""
    read = fields.Bool(missing=True)

class NotificationFilterSchema(Schema):
    """Notification filtering validation schema."""
    read = fields.Bool()
    type = fields.Str(validate=validate.OneOf(['meeting', 'task', 'followup', 'system']))
    page = fields.Int(missing=1, validate=validate.Range(min=1))
    limit = fields.Int(missing=50, validate=validate.Range(min=1, max=100))

class BulkNotificationUpdateSchema(Schema):
    """Bulk notification update validation schema."""
    notification_ids = fields.List(fields.Str(required=True), required=True)
    read = fields.Bool(missing=True)
