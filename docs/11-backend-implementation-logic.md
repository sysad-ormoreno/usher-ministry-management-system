from datetime import datetime, timedelta
from fastapi import HTTPException, status

def validate_sunday_slots(arrival_time: datetime, slots: list):
    """
    Business Logic: 30-minute grace period check. 
    Called during POST /registrations and PATCH /registrations.
    """
    # 30-minute window for operational readiness
    GRACE_WINDOW = timedelta(minutes=30)
    
    for slot in slots:
        # Check if arrival is past the start time + grace period
        if arrival_time > (slot.start_time + GRACE_WINDOW):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    f"Late Arrival: {arrival_time.strftime('%I:%M %p')} exceeds "
                    f"{slot.slot_name} cutoff ({ (slot.start_time + GRACE_WINDOW).strftime('%I:%M %p') })."
                )
            )
    return True
