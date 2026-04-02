"""
FILE: routers/registrations.py
SOURCE DOC: docs/11-backend-implementation-logic.md
DEPENDENCIES: models.User, models.ServiceSlot, models.Registration
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from .. import models, database

router = APIRouter(
    prefix="/registrations",
    tags=["Registrations"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. GET: See who is signed up for a specific date
@router.get("/")
def get_registrations(service_date: date, db: Session = Depends(get_db)):
    return db.query(models.Registration).filter(
        models.Registration.service_date == service_date
    ).all()

# 2. POST: The actual "Sign Up" logic
@router.post("/")
def sign_up_for_service(user_id: int, slot_id: int, service_date: date, db: Session = Depends(get_db)):
    # VALIDATION 1: Does the user exist?
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # VALIDATION 2: Does the slot exist?
    slot = db.query(models.ServiceSlot).get(slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="Service slot not found")

    # ACTION: Create the record
    new_reg = models.Registration(
        user_id=user_id,
        slot_id=slot_id,
        service_date=service_date,
        state="PENDING" # Default state from our logic doc
    )
    
    db.add(new_reg)
    db.commit()
    db.refresh(new_reg)
    return new_reg
