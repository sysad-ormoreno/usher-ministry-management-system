"""
FILE: database.py
SOURCE DOC: docs/00-architecture-decisions.md
DESCRIPTION: Manages the SQLAlchemy engine and session local factory for SQLite.
"""

from sqlalchemy import create_all, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This creates a local SQLite database file named 'usher_app.db'
SQLALCHEMY_DATABASE_URL = "sqlite:///./usher_app.db"

# The engine is the actual connection to the database
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Each instance of the SessionLocal class will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the class we will inherit from to create our Models
Base = declarative_base()
