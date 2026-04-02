# 04-data-model.md

## 1. Core Entities

### **Users & Profiles**
- **users:**
    - `id` (UUID, PK)
    - `email` (Unique, Nullable for Volunteers)
    - `google_id` (Unique, Nullable for Volunteers)
    - `role` (ENUM: ADMIN, CORE_LEADER, USHER, VOLUNTEER)
    - `status` (ENUM: ACTIVE, PENDING, DISABLED)
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
- **registration_slots:** (Many-to-Many for Sunday)
    - `registration_id` (FK)
    - `service_slot_id` (FK)

## 2. Communication & Audit
- **notifications:**
    - `id`, `user_id` (FK), `title`, `message`, `is_read`, `link_to_event_id`, `created_at`
- **audit_log:**
    - `id` (UUID, PK)
    - `actor_id` (FK to users) 
    - `target_user_id` (FK to users) 
    - `registration_id` (FK to registrations)
    - `action_type` (e.g., "STATUS_CHANGE", "SLOT_MOVE", "ASSIGN_AISLE", "PROFILE_EDIT")
    - `previous_state` (JSON) 
    - `new_state` (JSON) 
    - `timestamp`

## 3. Data Logic & Constraints

### **Registration Integrity**
- **Movement Policy:** When a registration is moved to a new date, the `event_instance_id` is updated. All associated `registration_slots` entries for the old date are purged; the user must re-select slots for the new date to ensure commitment time validity.
- **Lockout Calculation:** The 24-hour lockout is calculated programmatically: `lockout_timestamp = service_slot.start_time - 24 hours`.
- **The "No-Delete" Policy:** Registrations are never hard-deleted. "Withdrawals" are recorded as `state = CANCELLED` to maintain service history and burnout analytics.

### **Tenure & Profile Logic**
- **Tenure Accuracy:** `service_start_date` defaults to the date of first registration but must be manually editable by Admins to account for legacy members who served before the app's launch.
- **Profile Corrections:** Any administrative change to a user's name, phone, or service date must generate a `PROFILE_EDIT` entry in the `audit_log`.

### **Volunteer vs. Member Logic**
- **Volunteer:** Identified via `phone_number`. `google_id` remains NULL.
- **The "Link" Rule:** If a Volunteer joins as a Member, the Admin updates the record with a `google_id` and changes the role to `USHER`.

### **Recovery & History Logic**
- **Undo Capability:** System allows reverting changes by applying `previous_state` from the most recent `audit_log` entry.
- **Transparency:** Leaders can view the `audit_log` per registration to track state changes (e.g., who changed a status from ABSENT to PRESENT).

### **Privacy Layer** - **Ushers:** API returns aggregate counts of `registrations` where `state != CANCELLED`.
- **Leaders:** API joins `registrations` with `user_profiles` for full identity visibility.
