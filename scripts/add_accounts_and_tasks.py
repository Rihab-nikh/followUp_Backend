"""
Add three accounts with same password and create tasks for Abla

Usage:
  & .venv\Scripts\python.exe .\extracted_backend\extracted_backend\followup-backend\scripts\add_accounts_and_tasks.py

This script uses the project's models and DB utilities. Safe to run multiple
times when using the mock DB; duplicate email inserts will be ignored if
indexing/enforcement occurs.
"""
from datetime import datetime
import sys
from pathlib import Path

# Ensure package root on sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app import create_app
from app.utils.password_helper import hash_password
from app.utils.db import create_indexes, get_collection, get_db
from app.models.user import User
from app.models.task import Task


def safe_insert_user(email, full_name, role, password_plain):
    """Create user if not exists; return user id."""
    col = get_collection('users')
    existing = col.find_one({'email': email})
    if existing:
        print(f"User already exists: {email} -> id={existing.get('_id')}")
        return existing.get('_id')

    hashed = hash_password(password_plain)
    user = User(email=email, password=hashed, full_name=full_name, role=role)
    uid = user.create()
    print(f"Created user {full_name} ({email}) -> id={uid}")
    return uid


def create_task_for_user(user_id, title, description, due_date_str, tags=None, assignee=None, assignee_user_id=None):
    t = Task(
        user_id=user_id,
        title=title,
        description=description,
        meeting_id=None,
        assignee=assignee,
        assignee_user_id=assignee_user_id,
        due_date=due_date_str,
        priority='medium',
        status='todo',
        tags=tags or []
    )
    tid = t.create()
    print(f"Created task -> id={tid} title={title} due={due_date_str}")
    return tid


def main():
    app = create_app()
    with app.app_context():
        # Ensure indexes
        create_indexes()

        pwd = 'Leviathan@123*'

        # Create users
        users = {}
        users['Wassil Merad'] = safe_insert_user(
            email='wassil.merad@axians.com',
            full_name='Wassil Merad',
            role='Chef de département',
            password_plain=pwd
        )

        users['Abla Benslimane'] = safe_insert_user(
            email='abla.benslimane@axians.com',
            full_name='Abla Benslimane',
            role='Responsable de projet',
            password_plain=pwd
        )

        users['Rihab NIKH'] = safe_insert_user(
            email='rihab.nikh@axians.com',
            full_name='Rihab NIKH',
            role='Ingenieur Avant-vente',
            password_plain=pwd
        )

        # Create tasks for Abla (dates normalized as YYYY-MM-DD)
        abla_id = users['Abla Benslimane']
        wassil_id = users['Wassil Merad']

        # Map days provided by user to concrete dates in November 2025
        # MARDI 4th November 2025
        create_task_for_user(
            user_id=abla_id,
            title='Prise de contact - STELLANTIS',
            description='Prise de contact avec le client STELLANTIS',
            due_date_str='2025-11-04',
            tags=['Wassil Merad'],
            assignee='Abla Benslimane',
            assignee_user_id=abla_id
        )

        # MERCREDI 5th Nov 2025 - 10:30 polydesign : Projet renouvellement serveurs
        create_task_for_user(
            user_id=abla_id,
            title='10:30 - PolyDesign: Projet renouvellement serveurs',
            description='Equipe: PolyDesign - projet de renouvellement serveurs',
            due_date_str='2025-11-05',
            tags=['Wassil Merad'],
            assignee='Abla Benslimane',
            assignee_user_id=abla_id
        )

        # MERCREDI 5th Nov 2025 - REUNION LEAR WIRING ... VISITE DE COURTOISIE
        create_task_for_user(
            user_id=abla_id,
            title='REUNION LEAR WIRING TRIM TFZ WIRING TAC - Visite de courtoisie (Projets 2026)',
            description='Visite de courtoisie pour projets 2026 - LEAR WIRING',
            due_date_str='2025-11-05',
            tags=['Wassil Merad'],
            assignee='Abla Benslimane',
            assignee_user_id=abla_id
        )

        # VENDREDI 7th Nov 2025 - REUNION MATIS (SAFRAN)
        create_task_for_user(
            user_id=abla_id,
            title='REUNION: MATIS (SAFRAN) - Prise de contact',
            description='Prise de contact avec MATIS / SAFRAN',
            due_date_str='2025-11-07',
            tags=['Wassil Merad'],
            assignee='Abla Benslimane',
            assignee_user_id=abla_id
        )

        # 11th Nov 2025 - mardi : Reunion COFICAB : Création de compte
        create_task_for_user(
            user_id=abla_id,
            title='Reunion COFICAB - Création de compte',
            description='Reunion COFICAB: création de compte client',
            due_date_str='2025-11-11',
            tags=['Wassil Merad'],
            assignee='Abla Benslimane',
            assignee_user_id=abla_id
        )

        # Print collections summary
        db = get_db()
        try:
            print('\nCollections now present:')
            print(', '.join(db.list_collection_names()))
        except Exception:
            if hasattr(db, '_collections'):
                print('\nCollections now present:')
                print(', '.join(db._collections.keys()))


if __name__ == '__main__':
    main()
