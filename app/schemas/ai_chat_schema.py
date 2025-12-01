"""
AI Chat validation schemas using Marshmallow
"""

from marshmallow import Schema, fields, validate
from datetime import datetime

class AIMessageSchema(Schema):
    """Individual AI message validation schema."""
    sender = fields.Str(required=True, validate=validate.OneOf(['user', 'ai']))
    text = fields.Str(required=True, validate=validate.Length(min=1, max=2000))
    timestamp = fields.DateTime(missing=datetime.utcnow)

class AIChatSessionSchema(Schema):
    """AI chat session validation schema."""
    id = fields.Str(dump_only=True)
    user_id = fields.Str(required=True)
    session_id = fields.Str(required=True)
    messages = fields.List(fields.Nested(AIMessageSchema), missing=list)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class AIMessageCreateSchema(Schema):
    """AI message creation validation schema."""
    message = fields.Str(required=True, validate=validate.Length(min=1, max=2000))
    session_id = fields.Str(missing=None)

class AIChatRequestSchema(Schema):
    """AI chat request validation schema."""
    message = fields.Str(required=True, validate=validate.Length(min=1, max=2000))
    session_id = fields.Str(missing=None)

class AIChatResponseSchema(Schema):
    """AI chat response validation schema."""
    response = fields.Str(required=True)
    session_id = fields.Str(required=True)
    language = fields.Str()
    timestamp = fields.DateTime()

class AIChatHistoryResponseSchema(Schema):
    """AI chat history response schema."""
    sessions = fields.List(fields.Nested(AIChatSessionSchema))
    pagination = fields.Dict()

class AIMessageResponseSchema(Schema):
    """AI message response schema."""
    sender = fields.Str()
    text = fields.Str()
    timestamp = fields.DateTime()

class AIChatSessionDeleteSchema(Schema):
    """AI chat session deletion validation schema."""
    session_id = fields.Str(required=True)
