# 09. Volunteer & Guest Management

**File:** 09-volunteer-management.md
**Status:** STABLE | **Domain:** Guest Access & Promotion Workflows

## 1. Objectives & Scope
* **Accessibility:** Provide a low-barrier entry for provincial or 
  senior members who do not utilize Google accounts.
* **Frictionless Interaction:** Enable registration and 
  self-management without a permanent account structure.
* **Data Reliability:** Ensure all guest activity is captured 
  for Core Leader analytics (burnout and reliability tracking).
* **Tenure Policy:** Volunteers **do not** accrue tenure milestones 
  (3/5/10 years). Milestone tracking is activated only upon 
  promotion to a Member (`USHER`) role.

## 2. Authentication & Identity Logic
* **Unique Identifier:** The `phone_number` serves as the primary 
  key within the `user_profiles` table for all guests.
* **The 4-Digit PIN:**
    * Generated automatically by the system during registration.
    * Displayed **once** on the confirmation screen with a 
      high-visibility "Save your PIN" warning.
    * Stored in the database using secure hashing (Argon2/Bcrypt).
* **Session Management:** Authorization is granted via a 
  short-lived (15-minute) JWT, scoped specifically to the 
  Volunteer's registration IDs.

## 3. Permitted Self-Service Actions
* **Profile Updates:** Volunteers may update their `arrival_time` 
  or `discipler_name` for an active registration.
* **Slot Modification:** Adjust Sunday slot selections (1st, 2nd, 
  or 3rd) within the **same calendar date**.
* **Withdrawal:** Transition the registration state to `CANCELLED`.
    * **Constraint:** Hard deletion is strictly disabled to 
      maintain historical reliability data.

## 4. Operational Guardrails
* **Movement Restriction:** Volunteers are prohibited from 
  "Moving" a registration to a different date or event instance.
* **Lockout Enforcement:** All self-service actions are disabled 
  24 hours prior to the specific slot start time.

## 5. Security & Privacy
* **Brute Force Mitigation:** Implement a strict rate limit 
  (e.g., 5 attempts per 10 minutes) on the Login endpoint.
* **PII Protection:** Volunteer contact details are exclusively 
  visible to `CORE_LEADER` and `ADMIN` roles.

## 6. Promotion & Account Linking
* **Transition Path:** When a Volunteer eventually authenticates 
  via Google, they trigger the **New Member Registration** flow.
* **Database Merge:** An Admin performs an "Account Link" by 
  mapping the `google_id` to the existing volunteer record.
* **Role Update:** The user role is elevated to `USHER`, 
  preserving all historical service data.
* **Tenure Initialization:** The Admin manually initializes the 
  `service_start_date`, with the discretion to backdate the 
  tenure to include prior volunteer service.

## 7. The Approval Gate (Member Security)
* **Default State:** All new Google-linked registrations default 
  to `status: PENDING`.
* **Human-in-the-Loop:** `PENDING` users are restricted to a 
  "Waiting Room" until a Core Leader manually verifies the account.
* **Bot Protection:** This step serves as the final defense 
  against automated spam or unauthorized entry.

## 8. Administrative Notifications
* **Trigger Event:** Completion of the Profile Setup Form by a 
  new Member or promoted Volunteer.
* **Target Audience:** All users with `ADMIN` or `CORE_LEADER` roles.
* **Content:** "New Member Registration: [Name] is awaiting 
  approval. Review profile to set Tenure Start Date."
* **Deep-Linking:** Notifications link directly to the 
  **User Directory** for immediate action.
