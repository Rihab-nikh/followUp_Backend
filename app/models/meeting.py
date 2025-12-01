"""
Meeting model for MongoDB
"""

from datetime import datetime
from bson import ObjectId
from ..utils.db import get_collection

def create_meeting_indexes():
    """Create indexes for meetings collection."""
    meetings = get_collection('meetings')
    meetings.create_index('user_id')
    meetings.create_index('date')
    meetings.create_index('status')
    meetings.create_index([('company', 'text'), ('contact', 'text'), ('subject', 'text')])
    return True

class Meeting:
    """Meeting model for business meeting management."""
    
    def __init__(self, user_id, company, contact, subject, date, time, 
                 duration=60, location='Virtual Meeting', status='scheduled', 
                 priority='medium', description=None, notes=None, 
                 attendees=None, tags=None, phone=None, email=None, 
                 company_address=None, _id=None, created_at=None, updated_at=None):
        # Preserve DB id if provided
        self._id = _id
        try:
            self.id = str(_id) if _id is not None else None
        except Exception:
            self.id = None

        self.user_id = user_id
        self.company = company
        self.contact = contact
        self.subject = subject
        self.description = description
        self.date = date  # Format: YYYY-MM-DD
        self.time = time  # Format: HH:MM AM/PM
        self.duration = duration
        self.location = location
        self.status = status  # scheduled, completed, cancelled
        self.priority = priority  # high, medium, low
        self.notes = notes
        self.attendees = attendees or []
        self.tags = tags or []
        self.phone = phone
        self.email = email
        self.company_address = company_address
        # Preserve timestamps if provided
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self):
        """Convert meeting object to dictionary."""
        return {
            'user_id': self.user_id,
            'company': self.company,
            'contact': self.contact,
            'subject': self.subject,
            'description': self.description,
            'date': self.date,
            'time': self.time,
            'duration': self.duration,
            'location': self.location,
            'status': self.status,
            'priority': self.priority,
            'notes': self.notes,
            'attendees': self.attendees,
            'tags': self.tags,
            'phone': self.phone,
            'email': self.email,
            'company_address': self.company_address,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def find_by_user(cls, user_id, status=None, date_from=None, date_to=None):
        """Find meetings by user with optional filters."""
        collection = get_collection('meetings')
        query = {'user_id': user_id}
        
        if status:
            query['status'] = status
        
        if date_from and date_to:
            query['date'] = {'$gte': date_from, '$lte': date_to}
        elif date_from:
            query['date'] = {'$gte': date_from}
        elif date_to:
            query['date'] = {'$lte': date_to}
        
        cursor = collection.find(query).sort('date', 1)
        return [cls(**meeting_data) for meeting_data in cursor]
    
    @classmethod
    def find_by_id(cls, meeting_id, user_id=None):
        """Find meeting by ID, optionally filtered by user."""
        collection = get_collection('meetings')
        query = {'_id': ObjectId(meeting_id) if isinstance(meeting_id, str) else meeting_id}
        if user_id:
            query['user_id'] = user_id
        
        meeting_data = collection.find_one(query)
        return cls(**meeting_data) if meeting_data else None
    
    @classmethod
    def find_upcoming(cls, user_id, days=7):
        """Find upcoming meetings within specified days."""
        collection = get_collection('meetings')
        from datetime import datetime, timedelta
        
        end_date = datetime.now() + timedelta(days=days)
        end_date_str = end_date.strftime('%Y-%m-%d')
        
        query = {
            'user_id': user_id,
            'status': 'scheduled',
            'date': {'$lte': end_date_str}
        }
        
        cursor = collection.find(query).sort('date', 1)
        return [cls(**meeting_data) for meeting_data in cursor]
    
    @classmethod
    def find_by_date(cls, user_id, date):
        """Find meetings by specific date."""
        collection = get_collection('meetings')
        query = {
            'user_id': user_id,
            'date': date
        }
        cursor = collection.find(query).sort('time', 1)
        return [cls(**meeting_data) for meeting_data in cursor]
    
    @classmethod
    def find_today(cls, user_id):
        """Find today's meetings."""
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        return cls.find_by_date(user_id, today)
    
    def create(self):
        """Create meeting in database."""
        collection = get_collection('meetings')
        meeting_data = self.to_dict()
        result = collection.insert_one(meeting_data)
        return str(result.inserted_id)
    
    def update(self, meeting_id, user_id, update_data):
        """Update meeting data."""
        collection = get_collection('meetings')
        meeting_id = ObjectId(meeting_id) if isinstance(meeting_id, str) else meeting_id
        update_data['updated_at'] = datetime.utcnow()
        
        result = collection.update_one(
            {'_id': meeting_id, 'user_id': user_id}, 
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    def delete(self, meeting_id, user_id):
        """Delete meeting."""
        collection = get_collection('meetings')
        meeting_id = ObjectId(meeting_id) if isinstance(meeting_id, str) else meeting_id
        
        result = collection.delete_one({
            '_id': meeting_id, 
            'user_id': user_id
        })
        return result.deleted_count > 0
    
    @classmethod
    def search_by_text(cls, user_id, search_text):
        """Search meetings by text across company, contact, and subject."""
        collection = get_collection('meetings')
        query = {
            'user_id': user_id,
            '$text': {'$search': search_text}
        }
        cursor = collection.find(query)
        return [cls(**meeting_data) for meeting_data in cursor]
    
    @classmethod
    def group_by_date(cls, user_id, start_date=None, end_date=None):
        """Group meetings by date for calendar view."""
        collection = get_collection('meetings')
        pipeline = [
            {'$match': {'user_id': user_id}},
            {'$group': {
                '_id': '$date',
                'meetings': {'$push': {
                    'id': '$_id',
                    'company': '$company',
                    'contact': '$contact',
                    'subject': '$subject',
                    'time': '$time',
                    'status': '$status',
                    'priority': '$priority'
                }},
                'count': {'$sum': 1}
            }},
            {'$sort': {'_id': 1}}
        ]
        
        if start_date and end_date:
            pipeline.insert(1, {'$match': {
                'date': {'$gte': start_date, '$lte': end_date}
            }})
        
        return list(collection.aggregate(pipeline))
