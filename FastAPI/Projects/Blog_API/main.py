# main.py

from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv

# Import components using the new structured path
from app import models
from app.database import engine
from app.routers import blog, user, authentication

# Load environment variables from .env file
load_dotenv()

# --- DATABASE SETUP ---
# Create the database tables defined in app/models.py
# This should be done only once at startup.
models.Base.metadata.create_all(bind=engine)

# --- APPLICATION INITIALIZATION ---
app = FastAPI(
    title="Blog API with SQLAlchemy and FastAPI",
    description="A modular and production-ready structure for a blog application.",
    version="1.0.0"
)

# --- ROUTER REGISTRATION ---
# Include all routers to make their endpoints active
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)

# --- ROOT ENDPOINT ---
@app.get('/')
def index():
    """Returns a simple message for the root endpoint (health check)."""
    return {'message':'Blog API is running.'}


# --- DEBUGGING / DEVELOPMENT RUNNER ---
if __name__ == "__main__":
    # Note: Using '0.0.0.0' or '127.0.0.1' is safer than '172.0.0.1' unless specific network setup is needed.
    # Using '127.0.0.1' (localhost) here.
    uvicorn.run(app, host='127.0.0.1', port=9000)