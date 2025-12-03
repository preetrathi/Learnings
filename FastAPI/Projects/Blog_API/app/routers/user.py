# app/routers/user.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.repository import user # Import the repository module

router = APIRouter(
    prefix='/user',
    tags=['Users']
)

# --- CREATE USER (POST) ---
@router.post('/', response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user and returns the user object.
    """
    return user.create(request, db)

# --- READ ONE USER (GET) ---
@router.get('/{id}', response_model=schemas.ShowUser)
def show_user(id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single user by ID, including their associated blogs.
    """
    # Use the specific user repository function
    return user.get_user_by_id(id, db)