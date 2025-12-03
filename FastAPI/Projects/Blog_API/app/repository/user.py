# app/repository/user.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from .. import schemas, models
from ..core.hashing import Hash # Relative import for Hashing utility

# --- CREATE USER ---
def create(request: schemas.UserCreate, db: Session) -> models.Users:
    """
    Creates a new user with a hashed password.

    :param request: The validated user creation data (name, email, password).
    :param db: The database session.
    :return: The newly created Users model object.
    """
    # Create the Users object, hashing the password before storing it
    new_user = models.Users(
        name=request.name, 
        email=request.email, 
        password=Hash.aragon2(request.password) # Hash the password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- READ ONE USER ---
def get_user_by_id(id: int, db: Session) -> models.Users:
    """
    Retrieves a user by their ID.

    :param id: The ID of the user to retrieve.
    :param db: The database session.
    :raises HTTPException: If the user is not found.
    :return: The requested Users model object.
    """
    # Fetch the user using their primary key ID
    user = db.query(models.Users).filter(models.Users.id == id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'User with the id {id} is not available'
        )
    return user

def get_user_by_email(email: str, db: Session) -> models.Users | None:
    """
    Retrieves a user by their email. Used primarily for authentication.

    :param email: The email of the user.
    :param db: The database session.
    :return: The Users model object or None if not found.
    """
    user = db.query(models.Users).filter(models.Users.email == email).first()
    return user