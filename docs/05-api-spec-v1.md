# 05-api-spec-v1.md

## 1. Authentication & Profile
- `POST /auth/google`: Exchanges Google Token for a JWT.
- `POST /auth/volunteer/login`: Validates `phone_number` + `edit_pin`. Returns a restricted JWT.
- `GET /me`: Returns the current User/Volunteer profile and Role.
- `PATCH /me/profile`: Update personal details (Phone, Birthday, Preferred Schedule).

## 2. Events & Slots
- `GET /events/upcoming`: 
    - **Params:** `type` (Sunday/Midweek/Special), `weeks` (2/4/8).
    - **Output:** Grouped list of events with aggregate counts (Ushers) or name lists (Leaders).
- `GET /events/{instance_id}`: Detailed view of a specific date, including slot availability.

## 3. Registrations (Ushers & Members)
- `POST /registrations`: 
    - **Body:** `event_instance_id`, `arrival_time`, `slot_ids[]`.
    - **Logic:** Validates 24hr lockout and "Sunday Rule" (Arrival <= Slot Start + 30m).
- `PATCH /registrations/{reg_id}`: 
    - **Actions:** Update `arrival_time` or `slot_ids`.
    - **Move Logic:** If `event_instance_id` changes, previous slot selections are wiped.
- `DELETE /registrations/{reg_id}`: Sets state to `CANCELLED`. (Subject to 24hr lockout).
- `GET /me/registrations`: Returns personal history of upcoming and past duties.

## 4. Volunteer Management (PIN-Protected)
- `POST /volunteers/register`: 
    - **Body:** `full_name`, `phone_number`, `discipler_name`, `event_instance_id`, `arrival_time`, `slot_ids[]`.
    - **Response:** Returns the generated `edit_pin`.
- `PATCH /volunteers/registrations/{reg_id}`: Allows a Volunteer (via Phone JWT) to edit or cancel their entry.

## 5. Core Leader & Admin Operations
- **Attendance & Roster:**
    - `GET /events/{instance_id}/roster`: Returns full list of registrants with phone/discipler data.
    - `PATCH /registrations/{reg_id}/status`: 
        - **Body:** `state` (PRESENT, ABSENT, EXCUSED).
        - **Side Effect:** Creates an `audit_log` entry.
- **Assignments:**
    - `PATCH /registrations/{reg_id}/assignment`: Toggles `is_aisle_leader`.
- **System Recovery:**
    - `POST /registrations/{reg_id}/revert`: Fetches the last `audit_log` entry and restores the previous `state` or `slots`.
- **Utilities:**
    - `GET /util/disciplers/search?q=`: Returns unique discipler names for UI autocomplete.

## 6. Notifications & Audit
- `GET /notifications`: List of unread alerts for the logged-in user.
- `PATCH /notifications/{id}/read`: Marks a single notification as read.
- `GET /audit-logs/{reg_id}`: Returns the modification history for a specific registration (Leader only).

## 7. Error Codes
- `403 Forbidden`: Attempting to edit/withdraw within the 24hr lockout window.
- `409 Conflict`: Attempting to register for a Special Event that has reached capacity.
- `422 Unprocessable Entity`: "Sunday Rule" violation (Arrival time too late for selected slot).
