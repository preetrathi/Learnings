# app/repository/blog.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from .. import models, schemas # Relative imports

# --- READ ALL ---
def get_all(db: Session) -> List[models.Blog]:
    """Retrieves all blog posts from the database."""
    blogs = db.query(models.Blog).all()
    return blogs

# --- CREATE ---
def create(request: schemas.BlogCreate, db: Session, user_id: int) -> models.Blog:
    """
    Creates a new blog post.

    :param request: The validated blog creation data (title, body).
    :param db: The database session.
    :param user_id: The ID of the authenticated user creating the blog.
    :return: The newly created Blog model object.
    """
    # Map Pydantic schema data to SQLAlchemy model, including the creator's ID
    new_blog = models.Blog(
        title=request.title, 
        body=request.body,
        user_id=user_id # Link the blog to the current user
    )
    
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog) # Refresh to get the auto-generated ID
    return new_blog

# --- DELETE ---
def destroy(id: int, db: Session):
    """
    Deletes a blog post by ID.

    :param id: ID of the blog to delete.
    :param db: The database session.
    :raises HTTPException: If the blog is not found.
    :return: Success message.
    """
    # Query for the blog using filter and get the query object
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog_query.first():
        # Raise 404 if no blog matches the ID
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Blog with the id {id} is not available'
        )
        
    # Perform the deletion
    blog_query.delete(synchronize_session=False)
    db.commit()
    
    return 'Blog deleted successfully'


# --- UPDATE ---
def update(id: int, request: schemas.BlogUpdate, db: Session) -> str:
    """
    Updates an existing blog post.

    :param id: ID of the blog to update.
    :param request: The validated update data.
    :param db: The database session.
    :raises HTTPException: If the blog is not found.
    :return: Success message.
    """
    # Get the query object to perform the update
    blog_query = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Blog with the id {id} is not available'
        )
    
    # Update the record with the new data from the request, excluding unset fields
    blog_query.update(request.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    
    return 'Blog updated successfully'

# --- READ ONE ---
def show(id: int, db: Session) -> models.Blog:
    """
    Retrieves a single blog post by ID.

    :param id: ID of the blog to retrieve.
    :param db: The database session.
    :raises HTTPException: If the blog is not found.
    :return: The requested Blog model object.
    """
    # Use .first() to retrieve the single object
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Blog with the id {id} is not available'
        )
        
    return blog