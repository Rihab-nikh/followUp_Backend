"""
Password hashing utilities using bcrypt
"""

import bcrypt
import secrets
import string

def hash_password(password):
    """Hash password using bcrypt."""
    # Generate salt rounds (12 rounds minimum for security)
    salt_rounds = 12
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=salt_rounds)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed_password):
    """Verify password against hash."""
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def generate_reset_token():
    """Generate password reset token."""
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(64))
    return token

def validate_password_strength(password):
    """Validate password strength requirements."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    # Check for at least one uppercase, one lowercase, and one digit
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    if not (has_upper and has_lower and has_digit):
        return False, "Password must contain at least one uppercase letter, one lowercase letter, and one digit"
    
    return True, "Password is strong"
