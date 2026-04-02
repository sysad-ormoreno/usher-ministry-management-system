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
    - `phone_number` (Unique Index - our primary key for Volunteers)
    - `edit_pin` (Hashed, 4-digit - for Volunteers)
    - `discipler_name`
    - `birthday`
    - `preferred_schedule` (Optional)
    - `created_at`

### **Events & Schedule**
- **event_templates:** (To generate weekly services automatically)
    - `id`, `name`, `type` (SUNDAY, MIDWEEK, SPECIAL), `default_target`
- **event_instances:**
    - `id` (PK)
    - `template_id` (FK)
    - `date` (Date)
    - `start_time`, `end_time`
    - `capacity_limit` (Mainly for Special Events)
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
    - `created_at`, `updated_at`
- **registration_slots:** (Many-to-Many for Sunday)
    - `registration_id` (FK)
    - `service_slot_id` (FK)

## 2. Communication & Audit
- **notifications:**
    - `id`, `user_id` (FK), `title`, `message`, `is_read`, `link_to_event_id`, `created_at`
- **audit_log:**
    - `id`, `actor_id` (User who did the change), `action` (e.g., "MOVED_REGISTRATION"), `target_id`, `timestamp`, `metadata` (JSON of old vs new values)

## 3. Data Logic & Constraints

### **Volunteer vs. Member Logic**
- **Volunteer:** Created in `users` with `role: VOLUNTEER` and `google_id: NULL`. Identified via `phone_number` in `user_profiles`.
- **Member:** Linked via `google_id`. 
- **The "Link" Rule:** If a Volunteer joins as a Member later, the Admin updates the existing `user` record with their `google_id` and changes the role to `USHER`.

### **The Sunday Logic**
- A Sunday `event_instance` has 3 `service_slots`.
- A single `registration` record can link to multiple `service_slots` via the `registration_slots` table (e.g., an usher serving 1st and 2nd slots).

### **The Privacy Layer (API View Logic)**
- **Public/Usher API View:** Aggregates `registrations` grouped by `service_slot_id` to return `current_count`. 
- **Leader API View:** Joins `registrations` with `user_profiles` to return names and phone numbers.
