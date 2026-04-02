# 13-volunteer-management-mvp.md

## 1. Goals
- **Accessibility:** Allow volunteers (provincial/senior members without Google accounts) to register and self-manage.
- **Low Friction:** Avoid full account creation while maintaining a "session" for edits.
- **Data Integrity:** Ensure volunteer activity is trackable by Core Leaders for burnout and reliability analytics.

## 2. Authentication & Identity
- **Primary ID:** The `phone_number` serves as the unique identifier in the `user_profiles` table.
- **The PIN:** 
    - System generates a **4-digit numeric PIN** upon initial registration.
    - PIN is displayed **once** on the confirmation screen with a "Save this PIN" warning.
    - Only the **Hashed PIN** is stored in the database (Argon2/Bcrypt).
- **Session Logic:** A Volunteer logs in using (Phone + PIN) to receive a short-lived (15-min) JWT specifically scoped for their own registration IDs.

## 3. Permitted Actions (Self-Service)
- **Edit Details:** Update `arrival_time` or `discipler_name`.
- **Modify Slots:** Update Sunday slot selections (1st, 2nd, 3rd) within the **same date**.
- **Withdrawal:** Change registration `state` to `CANCELLED`. 
    - **Constraint:** Hard deletion is disabled. The record remains in the DB for "Reliability" tracking.

## 4. Restricted Actions (Guardrails)
- **No Moving:** Volunteers **cannot** move their registration to a different date/event instance. 
    - *Reasoning:* Moving requires complex validation of new dates; if a volunteer needs to "Move," they must Withdraw and Re-register, or contact a Core Leader.
- **Lockout:** All actions are disabled 24 hours prior to the slot start time.

## 5. Security & Rate Limiting
- **Brute Force Protection:** Implement a strict rate limit (e.g., 5 attempts per 10 minutes) on the Phone + PIN login endpoint.
- **PII Protection:** Volunteer contact info is only visible to users with `CORE_LEADER` or `ADMIN` roles.

## 6. The "Upgrade" Path
- If a Volunteer eventually signs in with a Google Account, an Admin can "Link" the accounts by adding the `google_id` to the existing volunteer record, promoted them to the `USHER` role while preserving their entire service history.
