"""
FILE: routers/slots.py
SOURCE DOC: docs/11-backend-implementation-logic.md (Section 1: The Sunday Rule)
DEPENDENCIES: models.ServiceSlot
DESCRIPTION: Manages service times and capacity limits for Sunday rotations.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import time
from .. import models, database

router = APIRouter(
    prefix="/slots",
    tags=["Service Slots"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_all_slots(db: Session = Depends(get_db)):
    return db.query(models.ServiceSlot).all()

@router.post("/")
def create_slot(name: str, start_time: str, capacity: int = 15, db: Session = Depends(get_db)):
    try:
        t = time.fromisoformat(start_time)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid time format. Use HH:MM")
        
    new_slot = models.ServiceSlot(
        slot_name=name, 
        start_time=t, 
        capacity_limit=capacity
    )
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    
    # FIX: Changed 'new_user' to 'new_slot'
    return new_slot
