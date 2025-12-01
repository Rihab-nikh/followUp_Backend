"""
Input validation utilities
"""

import re
from email_validator import validate_email, EmailNotValidError

def validate_email_address(email):
    """Validate email address format."""
    try:
        valid = validate_email(email)
        return True, valid.email
    except EmailNotValidError as e:
        return False, str(e)

def validate_phone_number(phone):
    """Validate phone number format."""
    if not phone:
        return True, phone
    
    # Remove common formatting characters
    cleaned = re.sub(r'[\s\-\(\)\.]', '', phone)
    
    # Check if it's a valid phone number (basic validation)
    if not re.match(r'^[\+]?[1-9][\d]{0,15}$', cleaned):
        return False, "Invalid phone number format"
    
    return True, phone

def validate_date_format(date_str, format_pattern=r'^\d{4}-\d{2}-\d{2}$'):
    """Validate date format."""
    if not re.match(format_pattern, date_str):
        return False, "Invalid date format. Expected YYYY-MM-DD"
    
    try:
        from datetime import datetime
        datetime.strptime(date_str, '%Y-%m-%d')
        return True, date_str
    except ValueError:
        return False, "Invalid date. Please provide a valid date"

def validate_time_format(time_str, format_pattern=r'^\d{1,2}:\d{2}\s*(AM|PM)$'):
    """Validate time format."""
    if not re.match(format_pattern, time_str, re.IGNORECASE):
        return False, "Invalid time format. Expected HH:MM AM/PM"
    
    try:
        # Try to parse the time to ensure it's valid
        from datetime import datetime
        time_str_clean = re.sub(r'\s*(AM|PM)$', '', time_str, flags=re.IGNORECASE)
        datetime.strptime(time_str_clean, '%H:%M')
        return True, time_str
    except ValueError:
        return False, "Invalid time. Please provide a valid time"

def validate_enum_value(value, valid_values, field_name):
    """Validate enum value."""
    if value not in valid_values:
        return False, f"Invalid {field_name}. Must be one of: {', '.join(valid_values)}"
    return True, value

def sanitize_string(text, max_length=1000):
    """Sanitize string input."""
    if not text:
        return text
    
    # Remove potentially dangerous characters
    sanitized = re.sub(r'[<>"\'\\\/]', '', text)
    
    # Truncate if too long
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized

def validate_pagination_params(page, limit):
    """Validate pagination parameters."""
    page = int(page) if page else 1
    limit = int(limit) if limit else 20
    
    if page < 1:
        return False, "Page must be greater than 0"
    
    if limit < 1 or limit > 100:
        return False, "Limit must be between 1 and 100"
    
    return True, {'page': page, 'limit': limit}

def validate_search_query(query, max_length=100):
    """Validate search query."""
    if not query:
        return True, query
    
    if len(query) > max_length:
        return False, f"Search query too long. Maximum {max_length} characters"
    
    # Sanitize search query
    sanitized = re.sub(r'[<>"\'\\\/]', '', query)
    return True, sanitized
