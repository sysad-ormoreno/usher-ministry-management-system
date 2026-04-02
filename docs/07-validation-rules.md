# 11-validation-rules.md

## 1. User Eligibility
- **Active Status:** Only users with `status: ACTIVE` (Members) or a valid **Phone + PIN** session (Volunteers) can create or modify registrations.
- **Pending/Disabled:** These users can view the dashboard but all "Register," "Edit," and "Move" buttons must be server-side disabled.
- **Tenure Eligibility:** The `service_start_date` field is mandatory for `USHER` profiles during the initial Profile Setup Form but is hidden/omitted for `VOLUNTEER` profiles.

## 2. Timing & Lockout Rules
- **The 24-Hour Rule:** Edit and Withdraw actions are locked exactly 24 hours before the `service_slot.start_time`.
    - *Logic:* `now() < (slot_start_time - 24 hours)`.
- **The Sunday Rule (Commitment vs. Slot):** A Sunday slot is only selectable if the user's `arrival_time` is within the "Grace Window."
    - *Formula:* `arrival_time <= (slot_start_time + 30 minutes)`.
    - *Example:* Arrival 10:31 AM? 1st Slot (10:00 AM) is disabled. 2nd and 3rd are available.
- **Minimum Commitment:** Every Sunday registration must have at least **one** associated slot. A registration with zero slots is invalid.

## 3. Capacity & Availability
- **Special Events:** If `capacity_limit` is not NULL, the system must check `current_count < capacity_limit` before accepting a `POST`.
- **Sunday Targets:** The `target_count` (e.g., 15) is a visual guideline only; it does **not** hard-block registration unless a hard `capacity_limit` is explicitly added by an Admin.

## 4. Movement & Modification Logic
- **Parent-Child Integrity:** When moving a registration to a new `event_instance_id` (a different day), all existing `registration_slots` (the 1st, 2nd, 3rd selections) are cleared.
- **Re-Validation:** The "Sunday Rule" and "Lockout Rule" must be re-run against the *new* target date/time during a Move action.

## 5. Volunteer Security (PIN)
- **Edit PIN:** Volunteers must provide a **4-digit numeric PIN** at registration.
- **Modification Access:** Any `PATCH` or `DELETE` request for a volunteer registration must include the hashed PIN in the payload or a valid Phone-JWT for session-based editing.

## 6. Core Leader Overrides (Permissions)
- **Lockout Bypass:** Core Leaders and Admins are **exempt** from the 24-hour lockout. They can Move or Cancel registrations even 5 minutes before a service.
- **State Transitions:** Only Leaders can move a registration state from `REGISTERED` to `PRESENT`, `ABSENT`, or `EXCUSED`. Regular Ushers and Volunteers can only toggle between `REGISTERED` and `CANCELLED`.
- **Tenure Override:** Only **ADMIN** or **CORE_LEADER** roles can modify a `service_start_date` after the initial profile creation to correct legacy member data.

## 7. Profile Data Integrity
- **No Future Dates:** The `service_start_date` and `birthday` fields must be `date <= current_date`. Any attempt to set a future date must return a `422 Unprocessable Entity`.
- **Role Consistency:** A `VOLUNTEER` profile cannot have a `service_start_date`. If a Volunteer is promoted to `USHER`, the Admin must manually set this date during the promotion/linking process.
