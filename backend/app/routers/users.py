"""
FILE: routers/users.py
SOURCE DOC: docs/04-data-model-implementation.md (User Model)
DEPENDENCIES: models.User
DESCRIPTION: Handles Usher profiles, roles, and registration identity.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@router.post("/")
def create_user(name: str, phone: str, db: Session = Depends(get_db)):
    new_user = models.User(full_name=name, phone_number=phone)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
