"""
Meeting validation schemas using Marshmallow
"""

from marshmallow import Schema, fields, validate, post_load
from datetime import datetime

class MeetingSchema(Schema):
    """Meeting data validation schema."""
    id = fields.Str(dump_only=True)
    user_id = fields.Str(required=True)
    company = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    contact = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    subject = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(missing=None, validate=validate.Length(max=1000))
    date = fields.Str(required=True, validate=validate.Regexp(r'^\d{4}-\d{2}-\d{2}$'))
    time = fields.Str(required=True, validate=validate.Regexp(r'^\d{1,2}:\d{2}\s*(AM|PM)$'))
    duration = fields.Int(missing=60, validate=validate.Range(min=15, max=480))
    location = fields.Str(missing='Virtual Meeting', validate=validate.Length(max=200))
    status = fields.Str(missing='scheduled', validate=validate.OneOf(['scheduled', 'completed', 'cancelled']))
    priority = fields.Str(missing='medium', validate=validate.OneOf(['high', 'medium', 'low']))
    notes = fields.Str(missing=None, validate=validate.Length(max=2000))
    attendees = fields.List(fields.Str(), missing=list)
    tags = fields.List(fields.Str(), missing=list)
    phone = fields.Str(missing=None, validate=validate.Regexp(r'^[\+]?[1-9][\d]{0,15}$'))
    email = fields.Email(missing=None)
    company_address = fields.Str(missing=None, validate=validate.Length(max=300))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class MeetingCreateSchema(Schema):
    """Meeting creation validation schema."""
    company = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    contact = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    subject = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    description = fields.Str(missing=None, validate=validate.Length(max=1000))
    date = fields.Str(required=True, validate=validate.Regexp(r'^\d{4}-\d{2}-\d{2}$'))
    time = fields.Str(required=True, validate=validate.Regexp(r'^\d{1,2}:\d{2}\s*(AM|PM)$'))
    duration = fields.Int(missing=60, validate=validate.Range(min=15, max=480))
    location = fields.Str(missing='Virtual Meeting', validate=validate.Length(max=200))
    priority = fields.Str(missing='medium', validate=validate.OneOf(['high', 'medium', 'low']))
    notes = fields.Str(missing=None, validate=validate.Length(max=2000))
    attendees = fields.List(fields.Str(), missing=list)
    tags = fields.List(fields.Str(), missing=list)
    phone = fields.Str(missing=None, validate=validate.Regexp(r'^[\+]?[1-9][\d]{0,15}$'))
    email = fields.Email(missing=None)
    company_address = fields.Str(missing=None, validate=validate.Length(max=300))

class MeetingUpdateSchema(Schema):
    """Meeting update validation schema."""
    company = fields.Str(validate=validate.Length(min=1, max=200))
    contact = fields.Str(validate=validate.Length(min=1, max=100))
    subject = fields.Str(validate=validate.Length(min=1, max=200))
    description = fields.Str(validate=validate.Length(max=1000))
    date = fields.Str(validate=validate.Regexp(r'^\d{4}-\d{2}-\d{2}$'))
    time = fields.Str(validate=validate.Regexp(r'^\d{1,2}:\d{2}\s*(AM|PM)$'))
    duration = fields.Int(validate=validate.Range(min=15, max=480))
    location = fields.Str(validate=validate.Length(max=200))
    priority = fields.Str(validate=validate.OneOf(['high', 'medium', 'low']))
    notes = fields.Str(validate=validate.Length(max=2000))
    attendees = fields.List(fields.Str())
    tags = fields.List(fields.Str())
    phone = fields.Str(validate=validate.Regexp(r'^[\+]?[1-9][\d]{0,15}$'))
    email = fields.Email()
    company_address = fields.Str(validate=validate.Length(max=300))

class MeetingStatusUpdateSchema(Schema):
    """Meeting status update validation schema."""
    status = fields.Str(required=True, validate=validate.OneOf(['scheduled', 'completed', 'cancelled']))

class MeetingFilterSchema(Schema):
    """Meeting filtering validation schema."""
    status = fields.Str(validate=validate.OneOf(['scheduled', 'completed', 'cancelled']))
    date_from = fields.Str(validate=validate.Regexp(r'^\d{4}-\d{2}-\d{2}$'))
    date_to = fields.Str(validate=validate.Regexp(r'^\d{4}-\d{2}-\d{2}$'))
    company = fields.Str(validate=validate.Length(min=1))
    priority = fields.Str(validate=validate.OneOf(['high', 'medium', 'low']))
    page = fields.Int(missing=1, validate=validate.Range(min=1))
    limit = fields.Int(missing=20, validate=validate.Range(min=1, max=100))

class MeetingResponseSchema(Schema):
    """Meeting response schema for API."""
    id = fields.Str()
    company = fields.Str()
    contact = fields.Str()
    subject = fields.Str()
    description = fields.Str()
    date = fields.Str()
    time = fields.Str()
    duration = fields.Int()
    location = fields.Str()
    status = fields.Str()
    priority = fields.Str()
    notes = fields.Str()
    attendees = fields.List(fields.Str())
    tags = fields.List(fields.Str())
    phone = fields.Str()
    email = fields.Str()
    company_address = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class CalendarViewSchema(Schema):
    """Calendar view response schema."""
    date = fields.Str()
    meetings = fields.List(fields.Nested(MeetingResponseSchema))
    count = fields.Int()
