from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import time
from .. import models, database

router = APIRouter(
    prefix="/slots",
    tags=["Service Slots"]
)

# This is our 'Database Connection' tool
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. GET: See all available service times
@router.get("/")
def get_all_slots(db: Session = Depends(get_db)):
    return db.query(models.ServiceSlot).all()

# 2. POST: Add a new service time (Admin only eventually)
@router.post("/")
def create_slot(name: str, start_time: str, capacity: int = 15, db: Session = Depends(get_db)):
    # Convert string "08:00" into a Python time object
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
    return new_user
