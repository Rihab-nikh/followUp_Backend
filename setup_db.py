#!/usr/bin/env python3
"""
Database setup script to create indexes and initial data
"""

from app import create_app
from app.config import config
from app.utils.db import init_db, create_indexes
import os

def setup_database():
    """Setup database with indexes"""
    config_name = os.environ.get('FLASK_ENV', 'development')
    app = create_app(config[config_name])
    
    with app.app_context():
        print('Setting up database indexes...')
        if create_indexes():
            print('✅ Database indexes created successfully!')
        else:
            print('⚠️ Some indexes may have failed to create')
        
        print(f'✅ Database setup complete for: {app.config["MONGO_URI"]}')

if __name__ == '__main__':
    setup_database()