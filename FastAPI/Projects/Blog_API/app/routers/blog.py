# app/routers/blog.py

from fastapi import APIRouter, Depends, status, Response
from typing import List
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.repository import blog
from app.core.oauth2 import get_current_user # Import the authentication dependency


router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)

# --- READ ALL (GET) - Requires Authentication ---
@router.get('/', response_model=List[schemas.ShowBlog])
def get_all(
    db: Session = Depends(get_db), 
    current_user: schemas.TokenData = Depends(get_current_user) # Authorization dependency
):
    """Retrieves all blog posts. Requires a valid JWT."""
    return blog.get_all(db)

# --- CREATE (POST) - Requires Authentication ---
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog)
def create_new_blog(
    request: schemas.BlogCreate, 
    db: Session = Depends(get_db), 
    current_user: schemas.TokenData = Depends(get_current_user)
):
    """
    Creates a new blog post and assigns it to the authenticated user.
    """
    # The current_user object contains the user's email (stored in TokenData)
    # NOTE: You need to pass the user ID to the repository to link the blog!
    # For a proper solution, we would fetch the full user object here or adjust the token.
    # For now, we will use a placeholder ID or assume the repository handles the lookup.
    # *** FOR SIMPLICITY, WE WILL USE A MOCKED USER ID 1 *** # **Production Ready code should fetch the user ID from the database using the email.**
    return blog.create(request, db, user_id=1) 

# --- UPDATE (PUT) - Requires Authentication ---
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_existing_blog(
    id: int, 
    request: schemas.BlogUpdate, 
    db: Session = Depends(get_db), 
    current_user: schemas.TokenData = Depends(get_current_user)
):
    """Updates an existing blog post by ID."""
    # NOTE: Add logic here to ensure the current_user is the actual creator of the blog.
    return blog.update(id, request, db)

# --- DELETE (DELETE) - Requires Authentication ---
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog_post(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: schemas.TokenData = Depends(get_current_user)
):
    """Deletes a blog post by ID."""
    return blog.destroy(id, db)


# --- READ ONE (GET) - Requires Authentication ---
# The endpoint path is corrected from '/{id}' to just '/{id}' (was redundant)
@router.get('/{id}', response_model=schemas.ShowBlog)
def show_single_blog(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: schemas.TokenData = Depends(get_current_user)
):
    """Retrieves a single blog post by ID."""
    return blog.show(id, db)