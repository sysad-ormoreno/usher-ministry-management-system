"""
FILE: routers/reports.py
SOURCE DOC: New Requirement (Core Leader Birthday Dashboard & Tenure Milestones)
DEPENDENCIES: models.User
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import extract, func
from sqlalchemy.orm import Session
from datetime import date, timedelta
from .. import models, database

router = APIRouter(prefix="/reports", tags=["Reports"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/birthdays/summary")
def get_birthday_summary(db: Session = Depends(get_db)):
    # Added filter to ignore null birth_dates so the 'count' is accurate
    results = db.query(
        extract('month', models.User.birth_date).label('month'),
        func.count(models.User.id).label('count')
    ).filter(models.User.birth_date != None).group_by('month').all()
    
    # Transform to list of dicts so the Frontend gets clear keys
    return [{"month": int(r.month), "count": r.count} for r in results]

@router.get("/birthdays/{month_number}")
def get_birthdays_by_month(month_number: int, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(
        extract('month', models.User.birth_date) == month_number
    ).all()
    
    if not users:
        return [] # Return empty list instead of null

    return [
        {
            "name": u.full_name,
            "birthday": u.birth_date.strftime("%B %d") if u.birth_date else "N/A"
        } for u in users
    ]

@router.get("/tenure-audit")
def get_tenure_audit(db: Session = Depends(get_db)):
    today = date.today()
    users = db.query(models.User).filter(models.User.service_start_date != None).all()
    
    report = []
    milestone_targets = [3, 5, 10, 15, 20]

    for user in users:
        start = user.service_start_date
        total_days_served = (today - start).days
        years_served = total_days_served / 365.25
        
        past_milestone = max([m for m in milestone_targets if m <= years_served], default=0)
        next_milestone = min([m for m in milestone_targets if m > years_served], default=None)
        
        days_until = None
        if next_milestone:
            try:
                next_date = start.replace(year=start.year + next_milestone)
                days_until = (next_date - today).days
            except ValueError: # Leap year safety
                next_date = start + timedelta(days=next_milestone * 365.25)
                days_until = (next_date - today).days

        is_overdue = past_milestone > user.last_recognized_milestone

        report.append({
            "name": user.full_name,
            "years_served_exact": round(years_served, 2),
            "highest_eligible_milestone": past_milestone, 
            "last_recognized_in_db": user.last_recognized_milestone,
            "status": "OVERDUE RECOGNITION" if is_overdue else "UP TO DATE",
            "next_upcoming_milestone": next_milestone,
            "days_until_next": days_until
        })
        
    return report
