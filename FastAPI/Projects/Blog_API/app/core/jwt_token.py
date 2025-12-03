# app/core/jwt_token.py

from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from app import schemas

load_dotenv()

# --- CONFIGURATION (Loaded from .env) ---
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))


def create_access_token(data: dict) -> str:
    """
    Creates a new JWT access token.

    :param data: Dictionary containing the payload (e.g., {'sub': user_email}).
    :return: The encoded JWT string.
    """
    to_encode = data.copy()
    # Set the token expiration time
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire}) # Add expiration time to the payload
    
    # Encode the payload into a JWT
    encoded_jwt = jwt.encode(
        to_encode, 
        SECRET_KEY, 
        algorithm = ALGORITHM
    )

    return encoded_jwt


def verify_token(token: str, credentials_exception) -> schemas.TokenData:
    """
    Verifies the JWT and extracts the token data.

    :param token: The JWT string from the request header.
    :param credentials_exception: The HTTP Exception to raise on failure.
    :raises JWTError: If the token is invalid or expired.
    :return: The validated TokenData schema.
    """
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract the user identifier (email, usually stored under 'sub')
        email: str = payload.get('sub') 
        
        if email is None:
            # If no email is found in the payload, token is invalid
            raise credentials_exception
            
        token_data = schemas.TokenData(email=email)
        
    except JWTError:
        # If decoding fails (e.g., wrong secret, expired token), raise exception
        raise credentials_exception

    return token_data