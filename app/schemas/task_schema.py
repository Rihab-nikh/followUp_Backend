"""
Task validation schemas using Marshmallow
"""

from marshmallow import Schema, fields, validate

class TaskSchema(Schema):
    """Task data validation schema."""
    id = fields.Str(dump_only=True)
    user_id = fields.Str(required=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(missing=None, validate=validate.Length(max=1000))
    meeting_id = fields.Str(missing=None)
    assignee = fields.Str(required=True, validate=validate.Length(max=10))
    assignee_user_id = fields.Str(missing=None)
    due_date = fields.Str(required=True, validate=validate.Regexp(r'^\d{4}-\d{2}-\d{2}$'))
    priority = fields.Str(required=True, validate=validate.OneOf(['high', 'medium', 'low']))
    status = fields.Str(missing='todo', validate=validate.OneOf(['todo', 'inprogress', 'done']))
    tags = fields.List(fields.Str(), missing=list)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    completed_at = fields.DateTime(dump_only=True)

class TaskCreateSchema(Schema):
    """Task creation validation schema."""
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(missing=None, validate=validate.Length(max=1000))
    meeting_id = fields.Str(missing=None)
    assignee = fields.Str(required=True, validate=validate.Length(max=10))
    assignee_user_id = fields.Str(missing=None)
    due_date = fields.Str(required=True, validate=validate.Regexp(r'^\d{4}-\d{2}-\d{2}$'))
    priority = fields.Str(required=True, validate=validate.OneOf(['high', 'medium', 'low']))
    tags = fields.List(fields.Str(), missing=list)

class TaskUpdateSchema(Schema):
    """Task update validation schema."""
    title = fields.Str(validate=validate.Length(min=1, max=200))
    description = fields.Str(validate=validate.Length(max=1000))
    meeting_id = fields.Str()
    assignee = fields.Str(validate=validate.Length(max=10))
    assignee_user_id = fields.Str()
    due_date = fields.Str(validate=validate.Regexp(r'^\d{4}-\d{2}-\d{2}$'))
    priority = fields.Str(validate=validate.OneOf(['high', 'medium', 'low']))
    status = fields.Str(validate=validate.OneOf(['todo', 'inprogress', 'done']))
    tags = fields.List(fields.Str())

class TaskStatusUpdateSchema(Schema):
    """Task status update validation schema."""
    status = fields.Str(required=True, validate=validate.OneOf(['todo', 'inprogress', 'done']))

class TaskFilterSchema(Schema):
    """Task filtering validation schema."""
    status = fields.Str(validate=validate.OneOf(['todo', 'inprogress', 'done']))
    priority = fields.Str(validate=validate.OneOf(['high', 'medium', 'low']))
    assignee = fields.Str(validate=validate.Length(max=10))
    due_date = fields.Str(validate=validate.Regexp(r'^\d{4}-\d{2}-\d{2}$'))
    page = fields.Int(missing=1, validate=validate.Range(min=1))
    limit = fields.Int(missing=20, validate=validate.Range(min=1, max=100))

class TaskResponseSchema(Schema):
    """Task response schema for API."""
    id = fields.Str()
    title = fields.Str()
    description = fields.Str()
    meeting_id = fields.Str()
    assignee = fields.Str()
    assignee_user_id = fields.Str()
    due_date = fields.Str()
    priority = fields.Str()
    status = fields.Str()
    tags = fields.List(fields.Str())
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    completed_at = fields.DateTime()

class KanbanBoardSchema(Schema):
    """Kanban board response schema."""
    status = fields.Str()
    title = fields.Str()
    tasks = fields.List(fields.Nested(TaskResponseSchema))
    count = fields.Int()

class TaskMoveSchema(Schema):
    """Task move to different status column."""
    new_status = fields.Str(required=True, validate=validate.OneOf(['todo', 'inprogress', 'done']))
