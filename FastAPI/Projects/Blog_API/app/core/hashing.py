# app/core/hashing.py

from passlib.context import CryptContext 

# Define the context for password hashing
# Schemes: Defines the hashing algorithm (argon2 is strong and recommended)
pwd_context = CryptContext(schemes=["argon2"], deprecated = "auto")

class Hash:
    """Utility class for password hashing and verification."""
    
    @staticmethod
    def aragon2(password: str) -> str:
        """Hashes a plain text password using argon2."""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        """Verifies a plain text password against a hashed password."""
        return pwd_context.verify(plain_password, hashed_password)