# app/core/oauth2.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from . import jwt_token
from app import schemas

# Define the OAuth2 scheme
# tokenUrl points to the endpoint where a client can exchange credentials for a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def get_current_user(token: str = Depends(oauth2_scheme)) -> schemas.TokenData:
    """
    FastAPI dependency to verify a JWT and get the current user's data.

    :param token: The token extracted by OAuth2PasswordBearer from the Authorization header.
    :raises HTTPException: If the token is invalid or missing.
    :return: The validated user data (email).
    """
    # Define the standardized exception for authorization failure
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail='Could not validate credentials', 
        headers={'WWW-Authenticate': 'Bearer'}
    )

    # Use the jwt_token utility to verify the token
    return jwt_token.verify_token(token, credentials_exception)