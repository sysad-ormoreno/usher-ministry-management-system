"""
FILE: routers/admin.py
SOURCE DOC: docs/12-system-configuration.md
DESCRIPTION: Global settings and administrative overrides.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, database

router = APIRouter(prefix="/admin", tags=["Admin & Settings"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/seed-settings")
def seed_system_settings(db: Session = Depends(get_db)):
    """
    Initializes the 'Control Panel' with default trainee rules.
    """
    defaults = [
        {
            "key": "TRAINEE_STREAK_REQUIRED", 
            "value": "6", 
            "description": "Number of weeks a trainee must serve before verification."
        },
        {
            "key": "STREAK_MODE", 
            "value": "STRICT", 
            "description": "STRICT (consecutive) or TOTAL (accumulated)."
        }
    ]

    for setting in defaults:
        existing = db.query(models.SystemSetting).filter(models.SystemSetting.key == setting["key"]).first()
        if not existing:
            new_setting = models.SystemSetting(**setting)
            db.add(new_setting)
    
    db.commit()
    return {"status": "System settings initialized", "defaults": defaults}

@router.get("/settings")
def get_all_settings(db: Session = Depends(get_db)):
    """Allows the Frontend to see the current rules."""
    return db.query(models.SystemSetting).all()
