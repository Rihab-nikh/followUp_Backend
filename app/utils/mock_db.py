"""
Mock in-memory database for development without MongoDB
"""

from datetime import datetime
from collections import defaultdict
import uuid

class MockDatabase:
    """Mock database that simulates MongoDB collections in memory."""
    
    def __init__(self):
        self._collections = defaultdict(list)
        self._indexes = defaultdict(dict)
    
    def __getitem__(self, collection_name):
        """Get a collection by name."""
        return MockCollection(collection_name, self)
    
    def list_collection_names(self):
        """List all collection names."""
        return list(self._collections.keys())

class MockCollection:
    """Mock MongoDB collection."""
    
    def __init__(self, name, db):
        self.name = name
        self._db = db
    
    def find_one(self, query):
        """Find one document matching the query."""
        documents = self._db._collections[self.name]
        for doc in documents:
            if self._matches_query(doc, query):
                return doc.copy()
        return None
    
    def find(self, query=None):
        """Find all documents matching the query."""
        if query is None:
            query = {}
        documents = self._db._collections[self.name]
        results = [doc.copy() for doc in documents if self._matches_query(doc, query)]
        return MockCursor(results)
    
    def insert_one(self, document):
        """Insert a document."""
        doc = document.copy()
        if '_id' not in doc:
            doc['_id'] = str(uuid.uuid4())
        self._db._collections[self.name].append(doc)
        
        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        
        return InsertResult(doc['_id'])
    
    def update_one(self, query, update):
        """Update one document."""
        documents = self._db._collections[self.name]
        for i, doc in enumerate(documents):
            if self._matches_query(doc, query):
                if '$set' in update:
                    documents[i].update(update['$set'])
                
                class UpdateResult:
                    def __init__(self, matched, modified):
                        self.matched_count = matched
                        self.modified_count = modified
                
                return UpdateResult(1, 1)
        
        class UpdateResult:
            def __init__(self, matched, modified):
                self.matched_count = matched
                self.modified_count = modified
        
        return UpdateResult(0, 0)
    
    def delete_one(self, query):
        """Delete one document."""
        documents = self._db._collections[self.name]
        for i, doc in enumerate(documents):
            if self._matches_query(doc, query):
                documents.pop(i)
                
                class DeleteResult:
                    def __init__(self, deleted):
                        self.deleted_count = deleted
                
                return DeleteResult(1)
        
        class DeleteResult:
            def __init__(self, deleted):
                self.deleted_count = deleted
        
        return DeleteResult(0)
    
    def create_index(self, keys, unique=False):
        """Create an index (mock - doesn't do anything)."""
        pass
    
    def aggregate(self, pipeline):
        """Simple aggregation (limited functionality)."""
        documents = self._db._collections[self.name]
        results = documents.copy()
        
        for stage in pipeline:
            if '$match' in stage:
                results = [doc for doc in results if self._matches_query(doc, stage['$match'])]
            elif '$sort' in stage:
                # Simple sort by first field
                field = list(stage['$sort'].keys())[0]
                direction = stage['$sort'][field]
                results.sort(key=lambda x: x.get(field, ''), reverse=(direction == -1))
        
        return results
    
    def _matches_query(self, document, query):
        """Check if a document matches a query."""
        if not query:
            return True
        
        for key, value in query.items():
            if key == '_id':
                # Handle ObjectId comparison
                doc_id = str(document.get('_id', ''))
                query_id = str(value)
                if doc_id != query_id:
                    return False
            elif key.startswith('$'):
                # Skip operators for simple matching
                continue
            elif isinstance(value, dict):
                # Handle operators like $ne, $gte, $lte, etc.
                if '$ne' in value and document.get(key) == value['$ne']:
                    return False
                if '$gte' in value and document.get(key, '') < value['$gte']:
                    return False
                if '$lte' in value and document.get(key, '') > value['$lte']:
                    return False
                if '$lt' in value and document.get(key, '') >= value['$lt']:
                    return False
            elif document.get(key) != value:
                return False
        
        return True

class MockCursor:
    """Mock MongoDB cursor."""
    
    def __init__(self, documents):
        self._documents = documents
    
    def sort(self, key, direction=1):
        """Sort documents."""
        self._documents.sort(
            key=lambda x: x.get(key, ''),
            reverse=(direction == -1)
        )
        return self
    
    def limit(self, count):
        """Limit results."""
        self._documents = self._documents[:count]
        return self
    
    def __iter__(self):
        """Iterate over documents."""
        return iter(self._documents)
    
    def __getitem__(self, key):
        """Get item by index or slice."""
        return self._documents[key]

# Global mock database instance
_mock_db = MockDatabase()

def get_mock_db():
    """Get the mock database instance."""
    return _mock_db
