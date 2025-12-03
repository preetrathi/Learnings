# app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base # Relative import from the current package

class Blog(Base):
    """SQLAlchemy model for the 'blogs' table."""
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index= True)
    title = Column(String)
    body = Column(String)
    # Foreign key linking a blog post to its creator (user)
    user_id = Column(Integer, ForeignKey('users.id')) 

    # Relationship to the Users table
    creator = relationship('Users', back_populates='blogs')

class Users(Base):
    """SQLAlchemy model for the 'users' table."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index= True)
    name = Column(String)
    email = Column(String, unique=True) # Added unique constraint for email
    password = Column(String)

    # Relationship to the Blog table
    blogs = relationship('Blog', back_populates='creator')