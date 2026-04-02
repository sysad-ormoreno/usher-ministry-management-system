"""
FILE: routers/reports.py
SOURCE DOC: New Requirement (Core Leader Birthday Dashboard)
DEPENDENCIES: models.User
"""

from fastapi import APIRouter, Depends
from sqlalchemy import extract, func
from sqlalchemy.orm import Session
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
            "birthday": u.birth_date.strftime("%B %d") # Results in "April 02"
        } for u in users
    ]
