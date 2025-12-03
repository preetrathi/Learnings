# app/routers/authentication.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app import schemas
from app.database import get_db
from app.repository import user # To fetch user by email
from app.core.hashing import Hash # To verify password
from app.core import jwt_token # To create JWT

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', response_model=schemas.Token)
def login(
    # OAuth2PasswordRequestForm is a standard FastAPI class for handling login requests
    request: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    Handles user login, verifies credentials, and returns an access token.
    """
    # 1. Fetch user by username (which is the email)
    user_db = user.get_user_by_email(request.username, db)
    
    # Check if the user exists
    if not user_db:
        # Raise 404 (or 401) for incorrect credentials
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Invalid Credentials"
        )
        
    # 2. Verify the password
    if not Hash.verify(request.password, user_db.password):
        # Raise 401 for incorrect password
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid Credentials"
        )
        
    # 3. Generate JWT Token
    # The subject ('sub') of the token is typically the unique user identifier (email)
    access_token = jwt_token.create_access_token(
        data={"sub": user_db.email}
    )
    
    # 4. Return the token in the standard OAuth2 format
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }