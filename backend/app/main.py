"""
FILE: main.py
SOURCE DOC: docs/00-architecture-decisions.md
DESCRIPTION: Entry point for FastAPI. Initializes database tables and includes all API routers.
"""

from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, slots, registrations, reports, audit, settings 

# Create the database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Usher Management System")

# This connects the "Hallways" to the main app
app.include_router(users.router)
app.include_router(slots.router)
app.include_router(registrations.router)
app.include_router(reports.router)
app.include_router(audit.router)
app.include_router(settings.router)

@app.get("/")
def read_root():
    return {"status": "Online", "message": "Usher API is running."}
