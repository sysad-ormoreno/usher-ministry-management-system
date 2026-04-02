"""
FILE: routers/reports.py
SOURCE DOC: New Requirement (Core Leader Birthday Dashboard & Tenure Milestones)
DEPENDENCIES: models.User
"""

from fastapi import APIRouter, Depends
from sqlalchemy import extract, func
from sqlalchemy.orm import Session
from datetime import date, timedelta # Added for Tenure math
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
    """
    Returns a list of months with the count of ushers having birthdays.
    Example: [{"month": 1, "count": 5}, {"month": 2, "count": 3}]
    """
    # We use 'extract' to get the month number from the date column
    results = db.query(
        extract('month', models.User.birth_date).label('month'),
        func.count(models.User.id).label('count')
    ).group_by('month').all()
    
    return results

@router.get("/birthdays/{month_number}")
def get_birthdays_by_month(month_number: int, db: Session = Depends(get_db)):
    """
    Returns names and birthdates (Month/Day only) for a specific month.
    """
    users = db.query(models.User).filter(
        extract('month', models.User.birth_date) == month_number
    ).all()
    
    # We transform the data here to HIDE the year
    return [
        {
            "name": u.full_name,
            "birthday": u.birth_date.strftime("%B %d") if u.birth_date else "N/A"
        } for u in users
    ]

@router.get("/tenure-audit")
def get_tenure_audit(db: Session = Depends(get_db)):
    """
    Calculates exact years served and identifies overdue milestones 
    based on the highest watermark principle.
    """
    today = date.today()
    users = db.query(models.User).filter(models.User.service_start_date != None).all()
    
    report = []
    milestone_targets = [3, 5, 10, 15, 20]

    for user in users:
        start = user.service_start_date
        total_days_served = (today - start).days
        years_served = total_days_served / 365.25
        
        # 1. Find highest milestone they qualify for (e.g., 10)
        past_milestone = max([m for m in milestone_targets if m <= years_served], default=0)
        
        # 2. Find the next milestone approaching
        next_milestone = min([m for m in milestone_targets if m > years_served], default=None)
        
        # 3. Calculate days until next (with Leap Year safety)
        days_until = None
        if next_milestone:
            try:
                next_date = start.replace(year=start.year + next_milestone)
                days_until = (next_date - today).days
            except ValueError:
                next_date = start + timedelta(days=next_milestone * 365.25)
                days_until = (next_date - today).days

        # 4. THE HIGHEST WATERMARK LOGIC
        # If they earned a 10 but last_recognized is 0, 3, or 5, they are OVERDUE.
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
