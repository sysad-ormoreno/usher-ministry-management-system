"""
FILE: routers/users.py
REVISION: Restored GET and Added Profile Fields for Reports
"""

from typing import Optional, List
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

# --- 1. THE RESTORED GET (List & Search) ---
@router.get("/")
def get_users(search: Optional[str] = None, role: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Returns a list of ushers. 
    - Filters by name or role if provided.
    """
    query = db.query(models.User)
    
    if search:
        query = query.filter(models.User.full_name.contains(search))
    
    if role:
        query = query.filter(models.User.role == role)
    
    return query.all()

# --- 2. GET SINGLE USER (Useful for details page) ---
@router.get("/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# --- 3. THE UPGRADED POST (Full Profile) ---
@router.post("/")
def create_user(
    full_name: str, 
    phone: str, 
    role: str = "VOLUNTEER", 
    birthday: Optional[date] = None, 
    service_start: Optional[date] = None,
    has_attended_101: bool = False, # <--- Added this
    db: Session = Depends(get_db)
):
    # Check if the phone number is already taken
    existing = db.query(models.User).filter(models.User.phone_number == phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone number already registered.")

    new_user = models.User(
        full_name=full_name,
        phone_number=phone,
        role=role,
        birth_date=birthday,
        service_start_date=service_start,
        last_recognized_milestone=0,
        is_active=True,
        # --- NEW FIELDS ---
        attended_101=has_attended_101, 
        is_trainee=True,      # Everyone starts as a trainee
        is_verified=False     # Leaders must confirm this later
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/me", response_model=schemas.UserRead)
async def read_user_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user
