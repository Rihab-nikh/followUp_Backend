"""
User model for MongoDB
"""

from datetime import datetime
from bson import ObjectId
from ..utils.db import get_collection, normalize_id

def create_user_index():
    """Create indexes for users collection."""
    users = get_collection('users')
    users.create_index('email', unique=True)
    return True

class User:
    """User model for authentication and preferences.

    This model is designed to be compatible with both the real MongoDB
    documents (which contain an `_id`) and the mock DB used in development.
    It preserves `_id` (and `id`) and timestamps when loading from the DB so
    controller code can access `user._id` or `user.id` as expected.
    """
    
    def __init__(self, email, password, full_name, role='user', avatar_initials=None,
                 preferences=None, _id=None, created_at=None, updated_at=None, last_login=None):
        self._id = _id
        # Expose a string id property for convenience
        try:
            self.id = str(_id) if _id is not None else None
        except Exception:
            self.id = None

        self.email = email
        self.password = password
        self.full_name = full_name
        self.role = role
        # If avatar_initials passed as list, join it; otherwise use provided value
        if isinstance(avatar_initials, (list, tuple)):
            self.avatar_initials = ''.join(avatar_initials)
        else:
            self.avatar_initials = avatar_initials or ''.join([p[:1] for p in full_name.split()[:2]]).upper()

        self.preferences = preferences or {
            'language': 'en',
            'theme': 'system',
            'notifications': True,
            'email_reminders': True
        }

        # Preserve timestamps when provided (e.g., when loading from DB)
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.last_login = last_login
    
    def to_dict(self):
        """Convert user object to dictionary."""
        return {
            'email': self.email,
            'password': self.password,
            'full_name': self.full_name,
            'role': self.role,
            'avatar_initials': self.avatar_initials,
            'preferences': self.preferences,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'last_login': self.last_login
        }
    
    @classmethod
    def find_by_email(cls, email):
        """Find user by email."""
        collection = get_collection('users')
        user_data = collection.find_one({'email': email})
        if not user_data:
            return None
        # Create user instance and preserve DB id and timestamps
        return cls(
            email=user_data.get('email'),
            password=user_data.get('password'),
            full_name=user_data.get('full_name'),
            role=user_data.get('role', 'user'),
            avatar_initials=user_data.get('avatar_initials'),
            preferences=user_data.get('preferences'),
            _id=user_data.get('_id'),
            created_at=user_data.get('created_at'),
            updated_at=user_data.get('updated_at'),
            last_login=user_data.get('last_login')
        )
    
    @classmethod
    def find_by_id(cls, user_id):
        """Find user by ID."""
        collection = get_collection('users')
        user_id = normalize_id(user_id)
        user_data = collection.find_one({'_id': user_id})
        if not user_data:
            return None
        # Create user instance and preserve DB id and timestamps
        return cls(
            email=user_data.get('email'),
            password=user_data.get('password'),
            full_name=user_data.get('full_name'),
            role=user_data.get('role', 'user'),
            avatar_initials=user_data.get('avatar_initials'),
            preferences=user_data.get('preferences'),
            _id=user_data.get('_id'),
            created_at=user_data.get('created_at'),
            updated_at=user_data.get('updated_at'),
            last_login=user_data.get('last_login')
        )
    
    def create(self):
        """Create user in database."""
        collection = get_collection('users')
        user_data = self.to_dict()
        result = collection.insert_one(user_data)
        # Store the inserted id on the instance for immediate use
        self._id = result.inserted_id
        try:
            self.id = str(result.inserted_id)
        except Exception:
            self.id = None
        return str(result.inserted_id)
    
    def update(self, user_id, update_data):
        """Update user data."""
        collection = get_collection('users')
        user_id = normalize_id(user_id)
        update_data['updated_at'] = datetime.utcnow()
        result = collection.update_one(
            {'_id': user_id}, 
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    def update_last_login(self, user_id):
        """Update last login timestamp."""
        collection = get_collection('users')
        user_id = normalize_id(user_id)
        result = collection.update_one(
            {'_id': user_id}, 
            {'$set': {'last_login': datetime.utcnow()}}
        )
        return result.modified_count > 0
    
    @classmethod
    def find_by_role(cls, role):
        """Find users by role."""
        collection = get_collection('users')
        cursor = collection.find({'role': role})
        return [cls(**user_data) for user_data in cursor]
