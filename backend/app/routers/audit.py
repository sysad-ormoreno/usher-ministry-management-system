"""
FILE: routers/audit.py
SOURCE DOC: docs/04-data-model.md (Universal Time Machine)
DEPENDENCIES: models.AuditLog
DESCRIPTION: Handles global state reversion and history tracking.
"""

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter(
    prefix="/audit",
    tags=["Audit & Revert"]
)

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/logs")
def get_audit_logs(limit: int = 50, db: Session = Depends(get_db)):
    """Returns the most recent activity logs for the Admin Dashboard."""
    return db.query(models.AuditLog).order_by(models.AuditLog.timestamp.desc()).limit(limit).all()

@router.post("/revert/{log_id}")
def global_revert(log_id: int, actor_id: int, db: Session = Depends(get_db)):
    """
    The 'Universal Undo' button. 
    Takes a previous_state JSON and applies it back to the target record.
    """
    # 1. Fetch the log entry
    log = db.query(models.AuditLog).filter(models.AuditLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Audit log entry not found")

    # 2. Map the target_type string to the actual SQLAlchemy Class
    model_map = {
        "USER": models.User,
        "REGISTRATION": models.Registration,
        "SERVICE_SLOT": models.ServiceSlot
    }
    
    target_model = model_map.get(log.target_type)
    if not target_model:
        raise HTTPException(status_code=400, detail=f"Invalid target type: {log.target_type}")

    # 3. Find the specific record being reverted
    record = db.query(target_model).filter(target_model.id == log.target_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="The record you are trying to revert no longer exists.")

    # 4. PERFORM THE REVERT (The Time Machine bit)
    try:
        old_values = json.loads(log.previous_state)
        for key, value in old_values.items():
            # setattr dynamically updates the column (e.g., record.role = "VOLUNTEER")
            setattr(record, key, value)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse history: {str(e)}")

    # 5. LOG THE REVERT ITSELF (Accountability)
    # We create a NEW log entry saying "User X reverted Action Y"
    revert_log = models.AuditLog(
        actor_id=actor_id,
        target_id=log.target_id,
        target_type=log.target_type,
        action_type="REVERT",
        previous_state=log.new_state, # In a revert, the 'old' is the 'new'
        new_state=log.previous_state
    )
    
    db.add(revert_log)
    db.commit()
    
    return {
        "status": "Success", 
        "message": f"Successfully reverted {log.target_type} (ID: {log.target_id}) to its previous state."
    }
