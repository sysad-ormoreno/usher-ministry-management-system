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

## 2. Audit Revert (The "Undo" System)
**Objective:** Allow Leaders to roll back a registration to its state prior to the most recent change.
**Mechanism:** `POST /registrations/{reg_id}/revert`

### Logic Workflow
1. **Fetch:** Retrieve the most recent `audit_log` entry where `registration_id == {reg_id}`.
2. **Extract:** Parse the `previous_state` JSON column.
3. **Validate:** Ensure the `actor_id` (the person clicking Revert) has the permissions to perform this action.
4. **Apply:** Update the `registrations` table (and `registration_slots` if applicable) using the values found in `previous_state`.
5. **Log:** Create a *new* audit entry of type `REVERT_ACTION` so the history remains linear.

### Reference Implementation (Python/FastAPI + SQLAlchemy)
```python
@router.post("/registrations/{reg_id}/revert")
async def revert_registration_state(reg_id: UUID, db: Session, current_user: User):
    # 1. Get the last meaningful change
    last_log = db.query(AuditLog).filter(
        AuditLog.registration_id == reg_id
    ).order_by(AuditLog.timestamp.desc()).first()

    if not last_log or not last_log.previous_state:
        raise HTTPException(status_code=404, detail="No revertible history found.")

    # 2. Extract the 'Snapshot' of the old data
    old_data = last_log.previous_state  # This is a JSON/Dict
    
    # 3. Target the registration
    registration = db.query(Registration).get(reg_id)
    
    # 4. Perform the Rollback
    # Example: restoring state and assignment
    registration.state = old_data.get("state", registration.state)
    registration.is_aisle_leader = old_data.get("is_aisle_leader", registration.is_aisle_leader)
    
    # 5. Handle Slot Restoration (If the change involved moving slots)
    if "slot_ids" in old_data:
        # Purge current slots and re-insert old ones
        db.query(RegistrationSlot).filter_by(registration_id=reg_id).delete()
        for s_id in old_data["slot_ids"]:
            db.add(RegistrationSlot(registration_id=reg_id, service_slot_id=s_id))

    db.commit()
    return {"message": "State successfully reverted to last known version."}
