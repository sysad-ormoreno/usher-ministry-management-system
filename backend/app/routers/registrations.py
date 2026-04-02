"""
FILE: routers/registrations.py
SOURCE DOC: docs/11-backend-implementation-logic.md
DEPENDENCIES: models.User, models.ServiceSlot, models.Registration
"""

import json # New: for the 'Snapshot' logic
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

# 3. PUT: Update attendance with an Audit Trail
@router.put("/{registration_id}")
def update_attendance(
    registration_id: int, 
    new_state: str, 
    admin_id: int, 
    db: Session = Depends(get_db)
):
    # 1. Fetch the existing record
    reg = db.query(models.Registration).get(registration_id)
    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found")

    # 2. CREATE SNAPSHOT (The Banking Ledger Entry)
    # We convert the current record into a dictionary/JSON string before changing it
    snapshot = json.dumps({
        "state": reg.state,
        "arrival_time": str(reg.arrival_time) if reg.arrival_time else None
    })

    # 3. CREATE THE AUDIT LOG
    log_entry = models.AuditLog(
        registration_id=reg.id,
        changed_by_id=admin_id,
        previous_state=snapshot,
        action_type="UPDATE"
    )
    db.add(log_entry)

    # 4. PERFORM THE UPDATE
    reg.state = new_state
    
    # COMMIT BOTH (Atomicity: Both succeed or both fail)
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
    # 1. Find the specific log entry
    log = db.query(models.AuditLog).filter(
        models.AuditLog.id == log_id,
        models.AuditLog.registration_id == registration_id
    ).first()
    
    if not log:
        raise HTTPException(status_code=404, detail="Audit log entry not found")

    # 2. Find the registration to be fixed
    reg = db.query(models.Registration).get(registration_id)
    if not reg:
        raise HTTPException(status_code=404, detail="Registration record not found")

    # 3. DECODE THE SNAPSHOT (Banking: Replaying the old tape)
    old_data = json.loads(log.previous_state)

    # 4. RESTORE DATA
    reg.state = old_data["state"]
    # If the snapshot had an arrival time, we restore it; otherwise, set to None
    reg.arrival_time = old_data.get("arrival_time") 

    # 5. LOG THE REVERSION ACTION
    reversion_log = models.AuditLog(
        registration_id=reg.id,
        changed_by_id=admin_id,
        previous_state=json.dumps({"info": "Reverting from log " + str(log_id)}),
        action_type="REVERT"
    )
    
    db.add(reversion_log)
    db.commit()
    db.refresh(reg)
    
    return {"message": "Revert successful", "new_state": reg.state}
