"""
Database initialization module to avoid circular imports.
Creates the SQLAlchemy instance used by both app.py and models.py.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
