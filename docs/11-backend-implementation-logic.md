# 11-backend-implementation-logic.md

## 1. The Sunday Rule (Grace Period Validation)
**Objective:** Prevent ushers from signing up for slots they arrive too late for.
**Constraint:** `arrival_time <= (slot_start_time + 30 minutes)`

### Reference Implementation (Python/FastAPI)
```python
from datetime import datetime, timedelta
from fastapi import HTTPException, status

def validate_sunday_slots(arrival_time: datetime, slots: list):
    """
    Business Logic: 30-minute grace period check.
    Called during POST /registrations and PATCH /registrations.
    """
    GRACE_WINDOW = timedelta(minutes=30)
    
    for slot in slots:
        # Check if arrival is past the start time + grace period
        if arrival_time > (slot.start_time + GRACE_WINDOW):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Late Arrival: {arrival_time.strftime('%H:%M')} exceeds {slot.slot_name} cutoff."
            )
    return True
