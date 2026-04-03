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

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/logs")
def get_audit_logs(limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.AuditLog).order_by(models.AuditLog.timestamp.desc()).limit(limit).all()

@router.post("/revert/{log_id}")
def global_revert(log_id: int, actor_id: int, db: Session = Depends(get_db)):
    log = db.query(models.AuditLog).filter(models.AuditLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Audit log entry not found")

    model_map = {
        "USER": models.User,
        "REGISTRATION": models.Registration,
        "SERVICE_SLOT": models.ServiceSlot
    }
    
    target_model = model_map.get(log.target_type)
    if not target_model:
        raise HTTPException(status_code=400, detail=f"Invalid target type: {log.target_type}")

    record = db.query(target_model).get(log.target_id)
    if not record:
        raise HTTPException(status_code=404, detail="The record no longer exists.")

    try:
        old_values = json.loads(log.previous_state)
        for key, value in old_values.items():
            if hasattr(record, key):
                setattr(record, key, value)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse history: {str(e)}")

    revert_log = models.AuditLog(
        actor_id=actor_id,
        target_id=log.target_id,
        target_type=log.target_type,
        action_type="REVERT",
        previous_state=json.dumps({"info": f"Global Revert from Log ID {log_id}"})
    )
    
    db.add(revert_log)
    db.commit()
    db.refresh(record) # Get the restored version
    
    # Return the restored record so the UI updates immediately
    return {
        "status": "Success",
        "restored_record": record,
        "new_log_id": revert_log.id
    }
