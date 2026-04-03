"""
FILE: routers/users.py
SOURCE DOC: docs/04-data-model-implementation.md (User Model)
DEPENDENCIES: models.User
DESCRIPTION: Handles Usher profiles, roles, and registration identity.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_users(search: Optional[str] = None, role: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.User)
    
    if search:
        query = query.filter(models.User.full_name.contains(search))
    
    if role:
        query = query.filter(models.User.role == role)
    
    return query.all()

@router.post("/")
def create_user(name: str, phone: str, db: Session = Depends(get_db)):
    # Basic check for existing user to prevent duplicates if you double-click
    existing = db.query(models.User).filter(models.User.full_name == name).first()
    if existing:
        return existing # Just return the existing one instead of crashing

    new_user = models.User(full_name=name, phone_number=phone)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
