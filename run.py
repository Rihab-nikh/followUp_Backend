#!/usr/bin/env python3
"""
FollowUp API Entry Point
"""

import os
from app import create_app
from app.config import config


def str_to_bool(value: str | None, default: bool = False) -> bool:
    """Interpret common truthy strings from env vars."""
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


# Determine configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config[config_name])

if __name__ == '__main__':
    # Disable reloader to avoid infinite restart loops on Windows
    # when antivirus/file indexers touch site-packages
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config['DEBUG'],
        use_reloader=False
    )
