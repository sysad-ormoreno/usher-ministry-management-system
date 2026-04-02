"""
FILE: main.py
SOURCE DOC: docs/00-architecture-decisions.md
DESCRIPTION: Entry point for FastAPI. Initializes database tables and includes all API routers.
"""

from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users # This imports your new user hallways

# Create the database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Usher Management System")

# This connects the /users routes to the main app
app.include_router(users.router)
app.include_router(slots.router)
app.include_router(registrations.router)

@app.get("/")
def read_root():
    return {"status": "Online", "message": "Usher API is running."}
