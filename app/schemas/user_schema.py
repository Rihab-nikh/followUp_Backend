"""
User validation schemas using Marshmallow
"""

from marshmallow import Schema, fields, validate, post_load
from datetime import datetime

class UserPreferencesSchema(Schema):
    """User preferences validation schema."""
    language = fields.Str(validate=validate.OneOf(['en', 'fr']), missing='en')
    theme = fields.Str(validate=validate.OneOf(['light', 'dark', 'system']), missing='system')
    notifications = fields.Boolean(missing=True)
    email_reminders = fields.Boolean(missing=True)

class UserSchema(Schema):
    """User data validation schema."""
    id = fields.Str(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    full_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    role = fields.Str(validate=validate.OneOf(['admin', 'user']), missing='user')
    avatar_initials = fields.Str(missing=None)
    preferences = fields.Nested(UserPreferencesSchema, missing=dict)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    last_login = fields.DateTime(dump_only=True)

class UserUpdateSchema(Schema):
    """User update validation schema."""
    email = fields.Email()
    full_name = fields.Str(validate=validate.Length(min=2, max=100))
    avatar_initials = fields.Str()
    preferences = fields.Nested(UserPreferencesSchema)

class UserLoginSchema(Schema):
    """User login validation schema."""
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class UserRegisterSchema(Schema):
    """User registration validation schema."""
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    full_name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    preferences = fields.Nested(UserPreferencesSchema, missing=dict)

class UserResponseSchema(Schema):
    """User response validation schema (excluding sensitive data)."""
    id = fields.Str()
    email = fields.Email()
    full_name = fields.Str()
    role = fields.Str()
    avatar_initials = fields.Str()
    preferences = fields.Nested(UserPreferencesSchema)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_login = fields.DateTime()

class PasswordChangeSchema(Schema):
    """Password change validation schema."""
    current_password = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=validate.Length(min=6))

class PasswordResetSchema(Schema):
    """Password reset validation schema."""
    email = fields.Email(required=True)

class PasswordResetConfirmSchema(Schema):
    """Password reset confirmation validation schema."""
    token = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=validate.Length(min=6))

class TokenRefreshSchema(Schema):
    """Token refresh validation schema."""
    refresh_token = fields.Str(required=True)
