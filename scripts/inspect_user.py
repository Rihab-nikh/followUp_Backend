r"""
Simple helper to inspect a user from the application's DB.

Usage:
    & .venv\Scripts\python.exe .\extracted_backend\extracted_backend\followup-backend\scripts\inspect_user.py abla.benslimane@axians.com

This prints the raw document and the `User` object produced by `find_by_email`.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app import create_app
from app.utils.db import get_collection, get_db
from app.models.user import User


def main():
    if len(sys.argv) < 2:
        print('Usage: inspect_user.py <email>')
        return

    email = sys.argv[1]
    app = create_app()
    with app.app_context():
        db = get_db()
        col = get_collection('users')
        raw = col.find_one({'email': email})
        print('Raw document:')
        print(raw)

        user = User.find_by_email(email)
        print('\nUser object:')
        print('type:', type(user))
        if user is None:
            print('User not found')
            return
        print('email:', getattr(user, 'email', None))
        print('id:', getattr(user, 'id', None))
        print('_id:', getattr(user, '_id', None))
        print('last_login:', getattr(user, 'last_login', None))
        print('created_at:', getattr(user, 'created_at', None))


if __name__ == '__main__':
    main()
