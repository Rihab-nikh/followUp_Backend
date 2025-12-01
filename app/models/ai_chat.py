"""
AI Chat History model for MongoDB
"""

from datetime import datetime
from bson import ObjectId
import uuid
from ..utils.db import get_collection

def create_ai_chat_indexes():
    """Create indexes for ai_chat collection."""
    ai_chat = get_collection('ai_chat')
    ai_chat.create_index('user_id')
    ai_chat.create_index('session_id')
    return True

class AIMessage:
    """Individual message in AI chat."""
    
    def __init__(self, sender, text, timestamp=None):
        self.sender = sender  # 'user' or 'ai'
        self.text = text
        self.timestamp = timestamp or datetime.utcnow()
    
    def to_dict(self):
        """Convert message to dictionary."""
        return {
            'sender': self.sender,
            'text': self.text,
            'timestamp': self.timestamp
        }

class AIChatSession:
    """AI Chat session model."""
    
    def __init__(self, user_id, messages=None, session_id=None, _id=None, created_at=None, updated_at=None):
        # Preserve DB id if provided
        self._id = _id
        try:
            self.id = str(_id) if _id is not None else None
        except Exception:
            self.id = None

        self.user_id = user_id
        # If messages are dicts from DB, convert to AIMessage objects
        self.messages = []
        if messages:
            for m in messages:
                if isinstance(m, AIMessage):
                    self.messages.append(m)
                elif isinstance(m, dict):
                    self.messages.append(AIMessage(m.get('sender'), m.get('text'), m.get('timestamp')))
        self.session_id = session_id or str(uuid.uuid4())
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self):
        """Convert chat session object to dictionary."""
        return {
            'user_id': self.user_id,
            'messages': [msg.to_dict() for msg in self.messages],
            'session_id': self.session_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def find_by_user(cls, user_id, limit=10, skip=0):
        """Find chat sessions by user."""
        collection = get_collection('ai_chat')
        query = {'user_id': user_id}
        cursor = collection.find(query).sort('updated_at', -1).skip(skip).limit(limit)
        return [cls(**chat_data) for chat_data in cursor]
    
    @classmethod
    def find_by_session_id(cls, session_id, user_id=None):
        """Find chat session by session ID."""
        collection = get_collection('ai_chat')
        query = {'session_id': session_id}
        if user_id:
            query['user_id'] = user_id
        
        chat_data = collection.find_one(query)
        return cls(**chat_data) if chat_data else None
    
    @classmethod
    def find_recent_sessions(cls, user_id, hours=24):
        """Find recent chat sessions within specified hours."""
        collection = get_collection('ai_chat')
        from datetime import datetime, timedelta
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        query = {
            'user_id': user_id,
            'updated_at': {'$gte': cutoff_time}
        }
        
        cursor = collection.find(query).sort('updated_at', -1)
        return [cls(**chat_data) for chat_data in cursor]
    
    def create(self):
        """Create chat session in database."""
        collection = get_collection('ai_chat')
        chat_data = self.to_dict()
        result = collection.insert_one(chat_data)
        return str(result.inserted_id)
    
    def add_message(self, message):
        """Add message to chat session."""
        self.messages.append(message)
        self.updated_at = datetime.utcnow()
        return self
    
    def save(self, session_id, user_id):
        """Save chat session with message history."""
        collection = get_collection('ai_chat')
        session_id = session_id if isinstance(session_id, str) else str(session_id)
        
        # Convert messages to dictionaries
        messages_data = [msg.to_dict() for msg in self.messages]
        
        result = collection.update_one(
            {'session_id': session_id, 'user_id': user_id},
            {
                '$set': {
                    'messages': messages_data,
                    'updated_at': datetime.utcnow()
                }
            },
            upsert=True
        )
        return result.modified_count > 0 or result.upserted_id is not None
    
    def delete_session(self, session_id, user_id):
        """Delete chat session."""
        collection = get_collection('ai_chat')
        session_id = session_id if isinstance(session_id, str) else str(session_id)
        
        result = collection.delete_one({
            'session_id': session_id,
            'user_id': user_id
        })
        return result.deleted_count > 0
    
    def delete_user_sessions(self, user_id):
        """Delete all chat sessions for a user."""
        collection = get_collection('ai_chat')
        result = collection.delete_many({'user_id': user_id})
        return result.deleted_count > 0
    
    @classmethod
    def get_or_create_session(cls, user_id, session_id=None):
        """Get existing session or create new one."""
        if session_id:
            session = cls.find_by_session_id(session_id, user_id)
            if session:
                return session
        
        # Create new session
        new_session = cls(user_id=user_id, session_id=session_id)
        return new_session
    
    def get_last_message(self, sender=None):
        """Get last message, optionally filtered by sender."""
        if not self.messages:
            return None
        
        if sender:
            messages = [msg for msg in self.messages if msg.sender == sender]
            return messages[-1] if messages else None
        
        return self.messages[-1]
    
    def get_message_history(self, limit=20):
        """Get recent message history."""
        return self.messages[-limit:] if self.messages else []
    
    def clear_history(self):
        """Clear message history."""
        self.messages = []
        self.updated_at = datetime.utcnow()
