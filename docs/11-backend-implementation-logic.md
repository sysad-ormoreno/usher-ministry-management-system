# 11-backend-implementation-logic.md

## 1. The Sunday Rule (Grace Period Validation)
**Objective:** Prevent ushers from signing up for slots they arrive too late for.
**Constraint:** arrival_time <= (slot_start_time + 30 minutes)

### Reference Implementation (Python/FastAPI)

    from datetime import datetime, timedelta
    from fastapi import HTTPException, status

    def validate_sunday_slots(arrival_time: datetime, slots: list):
        # 30-minute window for operational readiness
        GRACE_WINDOW = timedelta(minutes=30)
        
        for slot in slots:
            # Check if arrival is past the start time + grace period
            if arrival_time > (slot.start_time + GRACE_WINDOW):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Late Arrival: {arrival_time.strftime('%I:%M %p')} exceeds cutoff."
                )
        return True

---

## 2. Audit Revert (The "Undo" System)
**Objective:** Allow Leaders to roll back a registration to its state prior to the most recent change.
**Mechanism:** POST /registrations/{reg_id}/revert

### Logic Workflow
1. Fetch: Retrieve the most recent audit_log entry for registration_id.
2. Extract: Parse the previous_state JSON snapshot.
3. Validate: Ensure the actor_id has appropriate permissions.
4. Apply: Update the registration record with archived values.
5. Log: Create a new audit entry of type REVERT_ACTION.

### Reference Implementation (Python/SQLAlchemy)

    @router.post("/registrations/{reg_id}/revert")
    async def revert_registration_state(reg_id: UUID, db: Session, current_user: User):
        last_log = db.query(AuditLog).filter(
            AuditLog.registration_id == reg_id
        ).order_by(AuditLog.timestamp.desc()).first()

        if not last_log or not last_log.previous_state:
            raise HTTPException(status_code=404, detail="No revertible history found.")

        old_data = last_log.previous_state 
        registration = db.query(Registration).get(reg_id)
        
        registration.state = old_data.get("state", registration.state)
        registration.is_aisle_leader = old_data.get("is_aisle_leader", registration.is_aisle_leader)
        
        db.commit()
        return {"message": "Revert successful"}

---

## 3. Tenure Milestone Calculation
**Objective:** Programmatically determine 3, 5, and 10-year award eligibility.
**Requirement:** Account for leap years using a 365.25 day divisor.

### Reference Implementation (Python)

    from datetime import date

    def calculate_tenure_milestone(service_start_date: date):
        if not service_start_date:
            return None
            
        days_served = (date.today() - service_start_date).days
        years_served = days_served / 365.25

        if years_served >= 10: return "GOLD"
        if years_served >= 5: return "SILVER"
        if years_served >= 3: return "BRONZE"
        
        return None
