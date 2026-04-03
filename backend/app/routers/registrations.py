"""
FILE: routers/registrations.py
SOURCE DOC: docs/11-backend-implementation-logic.md
DEPENDENCIES: models.User, models.ServiceSlot, models.Registration
"""

import json 
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

# 2. POST: The actual "Sign Up" logic with Audit Trail
@router.post("/")
def sign_up_for_service(user_id: int, slot_id: int, service_date: date, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    slot = db.query(models.ServiceSlot).get(slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="Service slot not found")

    new_reg = models.Registration(
        user_id=user_id,
        slot_id=slot_id,
        service_date=service_date,
        state="PENDING" 
    )
    
    db.add(new_reg)
    db.commit() 
    db.refresh(new_reg)

    # Initial Snapshot for the Audit Log
    initial_snapshot = json.dumps({
        "state": new_reg.state,
        "arrival_time": None
    })
    
    log_entry = models.AuditLog(
        target_id=new_reg.id,
        target_type="REGISTRATION",
        actor_id=user_id,
        previous_state=initial_snapshot,
        action_type="CREATE"
    )
    
    db.add(log_entry)
    db.commit() 
    
    return new_reg

# 3. PUT: Update attendance with an Audit Trail
@router.put("/{registration_id}")
def update_attendance(
    registration_id: int, 
    new_state: str, 
    admin_id: int, 
    db: Session = Depends(get_db)
):
    reg = db.query(models.Registration).get(registration_id)
    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found")

    snapshot = json.dumps({
        "state": reg.state,
        "arrival_time": str(reg.arrival_time) if reg.arrival_time else None
    })

    log_entry = models.AuditLog(
        target_id=reg.id,
        target_type="REGISTRATION",
        actor_id=admin_id,
        previous_state=snapshot,
        action_type="UPDATE"
    )
    db.add(log_entry)

    reg.state = new_state
    db.commit()
    db.refresh(reg)
    return {"message": "Attendance updated", "audit_id": log_entry.id}

# 4. POST: Revert to a previous state
@router.post("/{registration_id}/revert/{log_id}")
def revert_registration(
    registration_id: int, 
    log_id: int, 
    admin_id: int, 
    db: Session = Depends(get_db)
):
    log = db.query(models.AuditLog).filter(
        models.AuditLog.id == log_id,
        models.AuditLog.target_id == registration_id,
        models.AuditLog.target_type == "REGISTRATION"
    ).first()
    
    if not log:
        raise HTTPException(status_code=404, detail="Audit log entry not found")

    reg = db.query(models.Registration).get(registration_id)
