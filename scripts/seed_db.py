r"""
Seed script to populate MongoDB (or mock DB) with sample French data.

Creates 3 users (in French) and sample meetings, tasks, notifications,
AI chat sessions and KPI metrics. Safe to run multiple times; clears
collections first when possible.

Usage: run from project root with the project's Python environment, for
example:
  & .venv\Scripts\python.exe .\extracted_backend\extracted_backend\followup-backend\scripts\seed_db.py
"""
from datetime import datetime, timedelta
import sys
import os
from pathlib import Path

# Ensure the followup-backend package root is on sys.path so `from app import ...`
# works when running this script from the repository root or other locations.
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from app import create_app
from app.utils.db import get_collection, create_indexes, get_db
from app.utils.password_helper import hash_password
from app.models.user import User
from app.models.meeting import Meeting
from app.models.task import Task
from app.models.notification import Notification
from app.models.ai_chat import AIChatSession, AIMessage
from app.models.kpi import KPIMetric


def clear_collection(name):
    """Try to clear a collection in both real and mock DBs."""
    col = get_collection(name)
    try:
        # pymongo collection
        col.delete_many({})
    except Exception:
        # mock collection: mutate underlying storage if available
        db = get_db()
        if hasattr(db, '_collections'):
            db._collections[name] = []


def seed(app):
    with app.app_context():
        # Ensure indexes exist
        create_indexes()

        # Collections to seed
        collections = ['users', 'meetings', 'tasks', 'notifications', 'ai_chat', 'kpi_metrics', 'companies']

        # Clear collections
        for c in collections:
            clear_collection(c)

        # Create users (French data)
        pwd = 'Passw0rd!'
        users_info = [
            {
                'full_name': 'Abla Benslimane',
                'email': 'abla.benslimane@exemple.com',
                'role': 'Commercial',
                'preferences': {'language': 'fr', 'theme': 'light', 'notifications': True, 'email_reminders': True}
            },
            {
                'full_name': 'Wassil Merad',
                'email': 'wassil.merad@axians-industrie.fr',
                'role': 'Chef de département',
                'preferences': {'language': 'fr', 'theme': 'dark', 'notifications': True, 'email_reminders': True}
            },
            {
                'full_name': 'Rihab NIKH',
                'email': 'rihab.nikh@exemple.com',
                'role': 'Ingénieur Pré-vente',
                'preferences': {'language': 'fr', 'theme': 'system', 'notifications': True, 'email_reminders': False}
            }
        ]

        created_users = {}
        for u in users_info:
            hashed = hash_password(pwd)
            user = User(email=u['email'], password=hashed, full_name=u['full_name'], role=u['role'], preferences=u.get('preferences'))
            user_id = user.create()
            created_users[u['full_name']] = user_id
            print(f"Created user {u['full_name']} -> id={user_id}")

        # Create some companies (minimal documents)
        companies_col = get_collection('companies')
        try:
            companies_col.insert_one({
                'name': 'Axians Industrie',
                'address': 'Parc Industriel, 31000 Toulouse, France',
                'contact': 'Wassil Merad',
                'phone': '+33 5 61 00 00 00'
            })
        except Exception:
            # Mock insert in case of mock DB
            db = get_db()
            if hasattr(db, '_collections'):
                db._collections['companies'].append({
                    '_id': 'axians-1',
                    'name': 'Axians Industrie',
                    'address': 'Parc Industriel, 31000 Toulouse, France',
                    'contact': 'Wassil Merad',
                    'phone': '+33 5 61 00 00 00'
                })

        # Create sample meetings (in French)
        meetings = []
        meetings.append(Meeting(
            user_id=created_users['Abla Benslimane'],
            company='Client Exemple SARL',
            contact='Jean Dupont',
            subject='Présentation de la solution',
            date=(datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
            time='10:00',
            duration=60,
            location='Bureau',
            status='scheduled',
            priority='high',
            description='Réunion commerciale pour présenter la nouvelle offre',
            phone='+33 6 12 34 56 78',
            email='jean.dupont@clientexemple.fr'
        ))

        meetings.append(Meeting(
            user_id=created_users['Wassil Merad'],
            company='Axians Industrie',
            contact='Equipe Technique',
            subject='Revue de projet',
            date=(datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'),
            time='14:30',
            duration=90,
            location='Siège Axians',
            status='scheduled',
            priority='medium',
            description='Revue hebdomadaire du projet Industriel'
        ))

        meetings.append(Meeting(
            user_id=created_users['Rihab NIKH'],
            company='Prospect Tech',
            contact='Sophie Martin',
            subject='Démonstration produit',
            date=(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            time='11:00',
            duration=45,
            location='Visio',
            status='scheduled',
            priority='low',
            description='Démonstration des capacités techniques'
        ))

        meeting_ids = []
        for m in meetings:
            mid = m.create()
            meeting_ids.append(mid)
            print(f"Created meeting -> id={mid} for user_id={m.user_id}")

        # Create sample tasks
        tasks = []
        tasks.append(Task(
            user_id=created_users['Abla Benslimane'],
            title='Envoyer proposition commerciale',
            description="Envoyer la proposition après la réunion",
            meeting_id=meeting_ids[0],
            assignee='Abla Benslimane',
            due_date=(datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d'),
            priority='high',
            status='todo'
        ))

        tasks.append(Task(
            user_id=created_users['Wassil Merad'],
            title='Préparer compte-rendu',
            description='Préparer le compte-rendu pour la revue de projet',
            meeting_id=meeting_ids[1],
            assignee='Wassil Merad',
            due_date=(datetime.now() + timedelta(days=6)).strftime('%Y-%m-%d'),
            priority='medium',
            status='todo'
        ))

        tasks.append(Task(
            user_id=created_users['Rihab NIKH'],
            title='Configurer démonstration',
            description='Préparer l’environnement de démonstration',
            meeting_id=meeting_ids[2],
            assignee='Rihab NIKH',
            due_date=(datetime.now() + timedelta(days=6)).strftime('%Y-%m-%d'),
            priority='medium',
            status='inprogress'
        ))

        task_ids = []
        for t in tasks:
            tid = t.create()
            task_ids.append(tid)
            print(f"Created task -> id={tid} title={t.title}")

        # Create notifications
        not1 = Notification(user_id=created_users['Abla Benslimane'], notification_type='meeting',
                            title='Rappel: réunion à venir', description='N’oubliez pas la réunion dans 3 jours', meeting_id=meeting_ids[0])
        not1_id = not1.create()
        print(f"Created notification -> id={not1_id}")

        not2 = Notification(user_id=created_users['Wassil Merad'], notification_type='task',
                            title='Tâche assignée', description='Vous avez une nouvelle tâche à préparer', task_id=task_ids[1])
        not2_id = not2.create()
        print(f"Created notification -> id={not2_id}")

        # Create AI chat sessions
        msg1 = AIMessage(sender='user', text='Bonjour, peux-tu résumer la réunion ?')
        msg2 = AIMessage(sender='ai', text='Bien sûr — voici le résumé...')
        chat = AIChatSession(user_id=created_users['Rihab NIKH'], messages=[msg1, msg2])
        chat_id = chat.create()
        print(f"Created AI chat session -> id={chat_id}")

        # Create KPI metrics
        kpi1 = KPIMetric(user_id=created_users['Abla Benslimane'], date=datetime.now().strftime('%Y-%m-%d'), metrics={
            'meetings_scheduled': 2,
            'meetings_completed': 0,
            'tasks_completed': 0,
            'tasks_pending': 1,
            'follow_ups_required': 0
        })
        kpi1_id = kpi1.create()
        print(f"Created KPI metric -> id={kpi1_id}")

        print('\nSeeding complete. Collections populated:')
        db = get_db()
        try:
            print(', '.join(db.list_collection_names()))
        except Exception:
            if hasattr(db, '_collections'):
                print(', '.join(db._collections.keys()))


if __name__ == '__main__':
    # Create Flask app with default config
    app = create_app()
    seed(app)
