# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv() # Load env vars for DATABASE_URL

# --- CONFIGURATION ---
# Correct path for a local file in the project root
# Using os.getenv for flexibility, falling back to local file path
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", 'sqlite:///./test.db')

# --- ENGINE CREATION ---
# Create the SQLAlchemy Engine
# The connect_args is essential for SQLite when used with multiple threads (like FastAPI)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# --- SESSION CREATION ---
# Configure the SessionLocal class to manage database sessions
SessionLocal = sessionmaker(
    bind=engine, 
    autocommit=False, 
    autoflush=False
)

# --- BASE CLASS ---
# Base class for all declarative SQLAlchemy models
Base = declarative_base()

# --- DATABASE DEPENDENCY ---
def get_db():
    """
    Dependency function to provide a database session to FastAPI route handlers.
    It ensures the session is created, yielded for use, and reliably closed afterward.
    """
    db = SessionLocal() # Create a new session
    try:
        yield db # Yield the session to the calling function
    finally:
        db.close() # Close the session to release the connection