"""
FILE: routers/users.py
REVISION: Added Profile Fields for Reports (Birthdays & Tenure)
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from .. import models, database

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_user(
    full_name: str, 
    phone: str, 
    role: str = "VOLUNTEER", 
    birthday: Optional[date] = None, 
    service_start: Optional[date] = None,
    db: Session = Depends(get_db)
):
    # 1. Check if the phone number is already taken (Our unique index)
    existing = db.query(models.User).filter(models.User.phone_number == phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone number already registered.")

    # 2. Create the User with all the "Report-Ready" columns
    new_user = models.User(
        full_name=full_name,
        phone_number=phone,
        role=role,
        birth_date=birthday,         # This feeds the Birthday Report
        service_start_date=service_start, # This feeds the Tenure Report
        last_recognized_milestone=0,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
