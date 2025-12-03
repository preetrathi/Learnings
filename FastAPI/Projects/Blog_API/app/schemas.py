# app/schemas.py

from typing import List, Optional
from pydantic import BaseModel

# --- REQUEST / CREATE SCHEMAS ---

class BlogCreate(BaseModel):
    """Schema for creating a new blog (input body)."""
    title: str
    body: str

class BlogUpdate(BaseModel):
    """Schema for updating an existing blog (PUT/PATCH)."""
    title: str | None = None
    body: str | None = None

class UserCreate(BaseModel):
    """Schema for creating a new user (input body)."""
    name: str
    email: str
    password: str

class Login(BaseModel):
    """Schema for user login credentials."""
    username: str # Used as the email
    password: str

# --- RESPONSE / OUTPUT SCHEMAS ---

class ShowUser(BaseModel):
    """Schema for showing user data (e.g., when viewing a blog creator)."""
    name: str
    email: str
    # When fetching a user, optionally include a list of their blogs
    blogs: List['ShowBlog'] = [] 

    class Config:
        from_attributes = True

class ShowBlog(BaseModel):
    """Schema for showing blog data (output response)."""
    title: str
    body: str
    # Include the creator details using the ShowUser schema
    creator: Optional[ShowUser] = None 
    
    class Config:
        from_attributes = True

# --- TOKEN SCHEMAS ---

class Token(BaseModel):
    """Schema for the JWT access token response."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema for the payload inside the JWT (used for verification)."""
    email: Optional[str] = None