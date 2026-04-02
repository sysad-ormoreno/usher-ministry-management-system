# 11-backend-implementation-logic.md

## 1. The Sunday Rule (Grace Period Validation)
**Objective:** Prevent ushers from signing up for slots they arrive too late for.  
**Constraint:** arrival_time <= (slot_start_time + 30 minutes)

### Reference Implementation (Python/FastAPI)
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

---

## 2. Audit Revert (The "Undo" System)
**Objective:** Allow Leaders to roll back a registration to its state prior to the most recent change.  
**Mechanism:** POST /registrations/{reg_id}/revert

### Logic Workflow
1. **Fetch:** Retrieve the most recent audit_log entry where registration_id == {reg_id}.
2. **Extract:** Parse the previous_state JSON column.
3. **Validate:** Ensure the actor_id (the person clicking Revert) has the permissions to perform this action.
4. **Apply:** Update the registrations table (and registration_slots if applicable) using the values found in previous_state.
5. **Log:** Create a new audit entry of type REVERT_ACTION so the history remains linear.

### Reference Implementation (Python/FastAPI + SQLAlchemy)
@router.post("/registrations/{reg_id}/revert")
async def revert_registration_state(reg_id: UUID, db: Session, current_user: User):
    # 1. Get the last meaningful change for this registration
    last_log = db.query(AuditLog).filter(
        AuditLog.registration_id == reg_id
    ).order_by(AuditLog.timestamp.desc()).first()

    if not last_log or not last_log.previous_state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No revertible history found for this record."
        )

    # 2. Extract the 'Snapshot' of the old data from the JSON column
    old_data = last_log.previous_state 
    
    # 3. Target the registration record
    registration = db.query(Registration).get(reg_id)
    if not registration:
        raise HTTPException(status_code=404, detail="Registration record not found.")
    
    # 4. Perform the Rollback (Selective updates)
    registration.state = old_data.get("state", registration.state)
    registration.is_aisle_leader = old_data.get("is_aisle_leader", registration.is_aisle_leader)
    registration.arrival_time = old_data.get("arrival_time", registration.arrival_time)
    
    # 5. Handle Slot Restoration (Atomic swap)
    if "slot_ids" in old_data:
        # Purge current slots and re-insert archived ones
        db.query(RegistrationSlot).filter_by(registration_id=reg_id).delete()
        for s_id in old_data["slot_ids"]:
            db.add(RegistrationSlot(registration_id=reg_id, service_slot_id=s_id))

    # 6. Finalize and Log
    db.commit()
    return {"message": "State successfully reverted to last known version."}

---

## 3. Tenure Milestone Calculation
**Objective:** Programmatically determine 3, 5, and 10-year award eligibility for the Leadership Dashboard.  
**Requirement:** Account for leap years using a 365.25 day divisor.

### Reference Implementation (Python)
def calculate_tenure_milestone(service_start_date: date):
    """
    Calculates milestone tier based on total days served.
    Logic: (Current Date - Start Date) / 365.25
    Returns: Tier string or None
    """
    if not service_start_date:
        return None
        
    days_served = (date.today() - service_start_date).days
    years_served = days_served / 365.25

    if years_served >= 10:
        return "GOLD"    # Legacy Milestone
    elif years_served >= 5:
        return "SILVER"  # Pillar Milestone
    elif years_served >= 3:
        return "BRONZE"  # Faithful Service Milestone
    
    return None
