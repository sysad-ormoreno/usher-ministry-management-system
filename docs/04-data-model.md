# 04. Data Model & Schema Specification
> **File:** `04-data-model.md`  
> **Status:** `STABLE` | **Domain:** `Database Architecture & Logic Constraints`

---

## 1. Term Definitions (Glossary)
To ensure clarity across all technical and operational workflows, the following terms are defined:

* **PII (Personally Identifiable Information):** Any data that can be used to identify a specific individual. In this system, this includes **Full Name**, **Phone Number**, **Birthday**, and **Discipler Name**.
* **Soft Delete:** A method of "deleting" data where the record remains in the database but is flagged (e.g., `state: CANCELLED`) so it no longer appears in active views. This preserves historical integrity.
* **Hard Delete:** The permanent removal of a record from the database. **(Prohibited for Registrations in this system).**
* **Audit Trail:** A chronological record of "Who did What and When." Powered by the `audit_log` table.
* **PK / FK:** Primary Key (Unique ID for a row) and Foreign Key (A link to a Primary Key in another table).

---

## 2. Core Entities

### **Users & Identity**
*   **users**:
    *   `id`: UUID (Primary Key).
    *   `email`: Unique (Nullable for Volunteers).
    *   `google_id`: Unique (Nullable for Volunteers).
    *   `role`: ENUM (`ADMIN`, `CORE_LEADER`, `USHER`, `VOLUNTEER`).
    *   `status`: ENUM (`ACTIVE`, `PENDING`, `DISABLED`).
    *   `last_recognized_milestone`: Integer (Default: 0). Tracks the highest tenure award already received.
*   **user_profiles**:
    *   `user_id`: Foreign Key to `users`.
    *   `first_name`, `last_name`: String.
    *   `phone_number`: Unique Index (Primary Key logic for Volunteers).
    *   `edit_pin`: Hashed 4-digit PIN (For Volunteer self-management).
    *   `discipler_name`: String (UI uses Autocomplete).
    *   `birthday`: Date.
    *   `service_start_date`: Date (Source for 3/5/10-year tenure calculations).

### **Events & Scheduling**
*   **event_templates**: `id`, `name`, `type` (`SUNDAY`, `MIDWEEK`, `SPECIAL`), `default_target`.
*   **event_instances**:
    *   `id`: Primary Key.
    *   `template_id`: Foreign Key to `event_templates`.
    *   `date`: Date.
    *   `start_time`, `end_time`: DateTime/Time.
    *   `capacity_limit`: Integer (Enforced for Special Events).
*   **service_slots** (Sunday Specific):
    *   `id`: Primary Key.
    *   `event_instance_id`: Foreign Key to `event_instances`.
    *   `slot_name`: `1st`, `2nd`, or `3rd`.
    *   `target_count`: Integer (Default: 15).

### **Registrations & Attendance**
*   **registrations**:
    *   `id`: Primary Key.
    *   `user_id`: Foreign Key to `users`.
    *   `event_instance_id`: Foreign Key (Parent for Movement Logic).
    *   `arrival_time`: Time (User commitment).
    *   `state`: ENUM (`REGISTERED`, `PRESENT`, `ABSENT`, `EXCUSED`, `CANCELLED`).
    *   `is_aisle_leader`: Boolean (Default: False).
    *   `updated_by`: Foreign Key to `users` (For Audit tracking).

---

## 3. Communication & Audit
*   **notifications**: `id`, `user_id`, `title`, `message`, `is_read`, `link_to_event_id`, `created_at`.
*   **audit_log** (The "Time Machine"):
    *   `id`: UUID (Primary Key).
    *   `actor_id`: Foreign Key to `users` (Who made the change).
    *   `target_id`: ID of the impacted record (User, Slot, or Reg).
    *   `target_type`: String/Table (e.g., "USER", "REGISTRATION").
    *   `action_type`: e.g., `UPDATE`, `REVERT`, `STATUS_CHANGE`.
    *   `previous_state` / `new_state`: JSON Snapshots for data restoration.

---

## 4. Data Logic & Constraints

### **Registration & Movement Policy**
*   **Clean Slate Rule:** When a registration is moved to a new date, the `event_instance_id` is updated, and all slot-specific sub-data for the old date is purged to force re-validation.
*   **Lockout Logic:** `lockout_timestamp = service_slot.start_time - 24 hours`.
*   **The "No-Delete" Policy:** To preserve reliability metrics, "Withdrawals" are strictly handled by updating `state` to `CANCELLED`. Hard deletes are prohibited.

### **Tenure & Milestone Logic**
*   **Highest Watermark Principle:** Updating `last_recognized_milestone` to a higher value (e.g., 5) automatically clears any "Overdue" flags for lower values (e.g., 3).
*   **Legacy Data:** `service_start_date` is manually adjustable by Admins to accommodate members who joined before system implementation.

### **Recovery & Privacy**
*   **Universal Revert:** The system uses `previous_state` JSON in the `audit_log` to restore any record to its prior state. Reverts are themselves logged as `action_type: REVERT`.
*   **Privacy Layer:** 
    *   **Ushers:** API returns aggregate registration counts only.
    *   **Leaders:** API joins `registrations` with `user_profiles` for full PII visibility.
