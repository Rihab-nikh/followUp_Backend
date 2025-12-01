"""Pytest configuration helpers.

Ensure the project root (followup-backend) is on sys.path so tests can
import the `app` package when pytest is executed from various working
directories or when pytest's automatic root detection picks a different
project root.
"""
import os
import sys


def _add_project_root_to_syspath():
    tests_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(tests_dir, '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


_add_project_root_to_syspath()
