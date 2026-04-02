# 04-data-model-v1.md

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
    - `discipler_name`
    - `birthday`
    - `preferred_schedule` (Optional)
    - `created_at`

### **Events & Schedule**
- **event_templates:** (For automatic generation)
    - `id`, `name`, `type` (SUNDAY, MIDWEEK, SPECIAL), `default_target`
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
    - `event_instance_id` (FK)
    - `arrival_time` (Commitment time)
    - `state` (ENUM: REGISTERED, PRESENT, ABSENT, EXCUSED, CANCELLED)
    - `is_aisle_leader` (Boolean, Default: False)
    - `updated_by` (FK to users) — Tracks the last person to modify the record
    - `created_at`, `updated_at`
- **registration_slots:** (Many-to-Many for Sunday)
    - `registration_id` (FK)
    - `service_slot_id` (FK)

## 2. Communication & Audit
- **notifications:**
    - `id`, `user_id` (FK), `title`, `message`, `is_read`, `link_to_event_id`, `created_at`
- **audit_log:**
    - `id` (UUID, PK)
    - `actor_id` (FK to users) — The Leader/User who performed the action
    - `target_user_id` (FK to users) — The Usher being modified
    - `registration_id` (FK to registrations)
    - `action_type` (e.g., "STATUS_CHANGE", "SLOT_MOVE", "ASSIGN_AISLE")
    - `previous_state` (JSON) — e.g., `{"state": "REGISTERED"}`
    - `new_state` (JSON) — e.g., `{"state": "ABSENT"}`
    - `timestamp`

## 3. Data Logic & Constraints

### **Volunteer vs. Member Logic**
- **Volunteer:** Identified via `phone_number` in `user_profiles`. `google_id` is NULL.
- **The "Link" Rule:** If a Volunteer becomes an official Member, the Admin updates their existing record with a `google_id` and changes the role to `USHER`.

### **Recovery & History Logic**
- **Undo Capability:** The system allows a "revert" by checking the `previous_state` in the `audit_log` and patching the `registrations` table back to that value.
- **Transparency:** Core Leaders can view the history of a registration to see who marked a member `ABSENT` or `PRESENT` and at what time.

### **The Sunday & Privacy Logic**
- **The Sunday Logic:** A single registration can link to multiple `service_slots` (e.g., serving 1st and 2nd slots).
- **Privacy Layer:** 
    - **Ushers:** Only see aggregate `current_count` from `registrations` joins. 
    - **Leaders:** Join `registrations` with `user_profiles` to access names and phone numbers.
