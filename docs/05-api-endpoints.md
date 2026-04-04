# 05. API Endpoints & Logic Specification
> **File:** `05-api-endpoints.md`  
> **Status:** `STABLE` | **Domain:** `Backend Interface & Business Logic`

---

## 1. Authentication & Profile Management
*   `POST /auth/google`: Exchanges a Google Identity Token for a System JWT.
*   `POST /auth/volunteer/login`: Validates `phone_number` + `edit_pin` for guest access. Returns a restricted-scope JWT.
*   `GET /me`: Returns the authenticated User/Volunteer profile, Role, and Status.
*   `PATCH /me/profile`: Update personal details (Phone, Birthday, Preferred Schedule).
    *   **Tenure Logic:** `service_start_date` is only accepted during the initial "New User" profile setup or for `USHER` roles.

---

## 2. Events & Slots Architecture
*   `GET /events/upcoming`: 
    *   **Params:** `type` (SUNDAY, MIDWEEK, SPECIAL), `weeks` (2, 4, or 8).
    *   **Privacy Logic:** Returns aggregate counts for `USHER` role; returns full name lists for `CORE_LEADER`.
*   `GET /events/{instance_id}`: Detailed view of a specific date, including real-time slot availability and targets.

---

## 3. Registrations (Members & Regular Ushers)
*   `POST /registrations`:
    *   **Body:** `event_instance_id`, `arrival_time`, `slot_ids[]`.
    *   **Validation:** Enforces the 24hr lockout and the **Sunday Rule** (Arrival $\le$ Slot Start + 30m).
*   `PATCH /registrations/{reg_id}`: Update `arrival_time` or `slot_ids`.
    *   **Movement Logic:** Changing the `event_instance_id` triggers a "Clean Slate" where previous slot selections are purged.
*   `DELETE /registrations/{reg_id}`: Performs a **Soft Delete** by setting the state to `CANCELLED`. (Subject to 24hr lockout).
*   `GET /me/registrations`: Returns the user's personal history of upcoming and past service duties.

---

## 4. Volunteer Management (Guest Access)
*   `POST /volunteers/register`:
    *   **Body:** `full_name`, `phone_number`, `discipler_name`, `event_instance_id`, `arrival_time`, `slot_ids[]`.
    *   **Output:** Returns the generated `edit_pin` for future self-management.
*   `PATCH /volunteers/registrations/{reg_id}`: Allows a Volunteer (via restricted JWT) to edit or cancel their guest entry.

---

## 5. Core Leader & Administrative Operations
*   **Roster & Attendance:**
    *   `GET /events/{instance_id}/roster`: Returns the full list of registrants with PII (Phone/Discipler) visible.
    *   `PATCH /registrations/{reg_id}/status`: Updates `state` (`PRESENT`, `ABSENT`, `EXCUSED`). Generates an `audit_log` entry.
*   **User Directory & Typo Correction:**
    *   `GET /users`: Searchable directory of all Profiles (Ushers + Volunteers).
    *   `PATCH /users/{profile_id}`: Allows Admins to fix names, phone numbers, or adjust `service_start_date` for tenure accuracy.
    *   `POST /users/{profile_id}/link-google`: Promotion tool to link a Volunteer profile to a `google_id`.
*   **Leadership & Recovery:**
    *   `PATCH /registrations/{reg_id}/assignment`: Toggles the `is_aisle_leader` boolean.
    *   `POST /registrations/{reg_id}/revert`: **The Undo Button.** Fetches the last `audit_log` entry to restore the previous state.
*   **Utility:**
    *   `GET /util/disciplers/search?q=`: Returns unique names for the UI Autocomplete component.

---

## 6. Notifications & Audit
*   `GET /notifications`: Fetches unread alerts (duty assignments, lockout reminders).
*   `PATCH /notifications/{id}/read`: Marks an alert as acknowledged.
*   `GET /audit-logs/{reg_id}`: Displays the full modification history for a specific registration (Leader-only).

---

## 7. Standardized Error Codes
*   `403 Forbidden`: Violation of the 24hr lockout window.
*   `409 Conflict`: Registration attempt on a Special Event that has reached capacity.
*   `422 Unprocessable Entity`: **Sunday Rule Violation** (Arrival time is too late for the selected slot).
