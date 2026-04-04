# 09. Volunteer & Guest Management
> **File:** `09-volunteer-management.md`  
> **Status:** `STABLE` | **Domain:** `Guest Access & Promotion Workflows`

---

## 1. Goals
- **Accessibility:** Allow volunteers (provincial/senior members without Google accounts) to register and self-manage.
- **Low Friction:** Avoid full account creation while maintaining a "session" for edits.
- **Data Integrity:** Ensure volunteer activity is trackable by Core Leaders for burnout and reliability analytics.
- **Tenure Policy:** Note that Volunteers **do not** accrue tenure milestones (3/5/10 years) while in this status. Tenure only begins upon promotion to a Member role.

---

## 2. Authentication & Identity
- **Primary ID:** The `phone_number` serves as the unique identifier in the `user_profiles` table.
- **The PIN:** - System generates a **4-digit numeric PIN** upon initial registration.
    - PIN is displayed **once** on the confirmation screen with a "Save this PIN" warning.
    - Only the **Hashed PIN** is stored in the database (Argon2/Bcrypt).
- **Session Logic:** A Volunteer logs in using (Phone + PIN) to receive a short-lived (15-min) JWT specifically scoped for their own registration IDs.

---

## 3. Permitted Actions (Self-Service)
- **Edit Details:** Update `arrival_time` or `discipler_name`.
- **Modify Slots:** Update Sunday slot selections (1st, 2nd, 3rd) within the **same date**.
- **Withdrawal:** Change registration `state` to `CANCELLED`. 
    - **Constraint:** Hard deletion is disabled. The record remains in the DB for "Reliability" tracking.

---

## 4. Restricted Actions (Guardrails)
- **No Moving:** Volunteers **cannot** move their registration to a different date/event instance. 
    - *Reasoning:* Moving requires complex validation of new dates; if a volunteer needs to "Move," they must Withdraw and Re-register, or contact a Core Leader.
- **Lockout:** All actions are disabled 24 hours prior to the slot start time.

---

## 5. Security & Rate Limiting
- **Brute Force Protection:** Implement a strict rate limit (e.g., 5 attempts per 10 minutes) on the Phone + PIN login endpoint.
- **PII Protection:** Volunteer contact info is only visible to users with `CORE_LEADER` or `ADMIN` roles.

---

## 6. The "Upgrade" & Promotion Path
- **Initiation:** If a Volunteer eventually signs in with a Google Account, they complete the **New Member Registration**.
- **Account Linking:** An Admin must "Link" the accounts by adding the `google_id` to the existing volunteer record.
- **Promotion:** The role is updated to `USHER`, preserving their entire service history.
- **Tenure Kick-off:** During this merge, the Admin manually sets the `service_start_date`. Leaders have the discretion to "backdate" this to include past Volunteer service or set it to the current date.

---

## 7. The Approval Gate (New Member Security)
- **Status: PENDING:** All new Google registrations (whether a new user or a promoted volunteer) default to `status: PENDING`.
- **Core Leader Review:** Users in `PENDING` status are blocked from registering for any upcoming slots. They remain in the "Waiting Room" until a Core Leader manually approves them.
- **Bot/Spam Protection:** This human-in-the-loop step ensures that only verified individuals enter the active roster, preventing bot-driven registration floods.

---

## 8. Leadership Notifications
- **Trigger:** When a new user completes the Profile Setup Form (New Member).
- **Action:** An automated notification is sent to all `ADMIN` and `CORE_LEADER` roles.
- **Content:** *"New Member Registration: [Name] is awaiting approval. Review profile to set Tenure Start Date."*
- **Deep Link:** The notification deep-links directly to the User Directory for immediate approval/rejection.
