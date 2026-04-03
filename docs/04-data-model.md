# 04-data-model.md

## 1. Core Entities

### **Users & Profiles**
- **users:**
    - `id` (UUID, PK)
    - `email` (Unique, Nullable for Volunteers)
    - `google_id` (Unique, Nullable for Volunteers)
    - `role` (ENUM: ADMIN, CORE_LEADER, USHER, VOLUNTEER)
    - `status` (ENUM: ACTIVE, PENDING, DISABLED)
    - `last_recognized_milestone` (Integer, Default: 0) — **Tracks the highest tenure award the usher has already received.**
- **user_profiles:**
    - `user_id` (FK to users)
    - `first_name`, `last_name`
    - `phone_number` (Unique Index - primary key for Volunteers)
    - `edit_pin` (Hashed, 4-digit - for Volunteers)
    - `discipler_name` (UI utilizes autocomplete based on existing entries)
    - `birthday`
    - `service_start_date` (Date - Used for 3/5/10-year tenure awards)
    - `preferred_schedule` (Optional)
    - `created_at`

### **Events & Schedule**
- **event_templates:** - `id`, `name`, `type` (SUNDAY, MIDWEEK, SPECIAL), `default_target`
- **event_instances:**
    - `id` (PK)
    - `template_id` (FK)
    - `date` (Date)
    - `start_time`, `end_time`
    - `capacity_limit` (For Special Events)
- **service_slots:** (Specific to Sunday)
    - `id` (PK)
    - `event_instance_id` (FK)
    - `slot_name` (1st, 2nd, 3rd)
    - `start_time`, `end_time`
    - `target_count` (Default: 15)

### **Registrations & Attendance**
- **registrations:**
    - `id` (PK)
    - `user_id` (FK)
    - `event_instance_id` (FK) — **Primary Parent for Movement Logic**
    - `arrival_time` (Commitment time)
    - `state` (ENUM: REGISTERED, PRESENT, ABSENT, EXCUSED, CANCELLED)
    - `is_aisle_leader` (Boolean, Default: False)
    - `updated_by` (FK to users)
    - `created_at`, `updated_at`

## 2. Communication & Audit
- **notifications:**
    - `id`, `user_id` (FK), `title`, `message`, `is_read`, `link_to_event_id`, `created_at`
- **audit_log:**
    - `id` (UUID, PK)
    - `actor_id` (FK to users) — **Who made the change?**
    - `target_id` (UUID/Int) — **ID of the impacted record (User, Slot, or Reg)**
    - `target_type` (String) — **Table name (e.g., "USER", "SERVICE_SLOT", "REGISTRATION")**
    - `action_type` (e.g., "UPDATE", "REVERT", "STATUS_CHANGE")
    - `previous_state` (JSON) — **Snapshot of data BEFORE the change**
    - `new_state` (JSON) — **Snapshot of data AFTER the change**
    - `timestamp`

## 3. Data Logic & Constraints

### **Search & Filtering Logic**
- **Fuzzy Name Search:** The User API supports a `search` query parameter for case-insensitive partial matching on `full_name`.
- **Role Filtering:** The User API supports a `role` query parameter for exact matches to isolate specific usher groups.

### **Registration Integrity**
- **Movement Policy:** When a registration is moved to a new date, the `event_instance_id` is updated. All associated `registration_slots` entries for the old date are purged.
- **Lockout Calculation:** The 24-hour lockout is calculated: `lockout_timestamp = service_slot.start_time - 24 hours`.
- **The "No-Delete" Policy:** Registrations are never hard-deleted. "Withdrawals" are recorded as `state = CANCELLED`.

### **Tenure & Profile Logic**
- **Tenure Accuracy:** `service_start_date` defaults to the date of first registration but is manually editable by Admins for legacy members.
- **Milestone Tracking:** The `last_recognized_milestone` uses the "Highest Watermark" principle. Updating this to a higher number (e.g., 10) automatically clears the "Overdue" status for all lower milestones (3, 5).
- **Profile Corrections:** Any administrative change to a user's name, phone, or service date must generate a `PROFILE_EDIT` entry in the `audit_log`.

### **Volunteer vs. Member Logic**
- **Volunteer:** Identified via `phone_number`. `google_id` remains NULL.
- **The "Link" Rule:** If a Volunteer joins as a Member, the Admin updates the record with a `google_id` and changes the role to `USHER`.

### **Recovery & History Logic (Universal Time Machine)**
- **Global Undo Capability:** Every administrative change triggers an Audit Log entry. The system provides a universal revert mechanism that applies the `previous_state` JSON back to the record identified by `target_id` and `target_type`.
- **Accountability:** Reverts are themselves logged as a new `action_type = "REVERT"` to ensure no "silent" changes occur.
- **Transparency:** Leaders can view the `audit_log` per entity to track the full history of changes.

### **Privacy Layer** 
- **Ushers:** API returns aggregate counts of `registrations` where `state != CANCELLED`.
- **Leaders:** API joins `registrations` with `user_profiles` for full identity visibility.
