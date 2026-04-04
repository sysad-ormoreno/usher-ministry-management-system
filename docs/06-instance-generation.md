# 06. Event Instance Generation
> **File:** `06-instance-generation.md`  
> **Status:** `STABLE` | **Domain:**   `Automation & Calendar Synchronization`

---

## 1. Objectives & Frequency
*   **Goal:** Maintain a rolling window of **8–12 weeks** of future events to facilitate long-term scheduling and usher availability planning.
*   **Automation Trigger:** A background worker (Cron Job) executes every **Monday at 00:00**.
*   **System of Record:** The PostgreSQL database is the authoritative "Source of Truth." The Google Calendar API acts as a "One-Way Mirror" for public visibility and personal calendar syncing.

---

## 2. Generation Logic

### **Sunday Services (Weekly Cycle)**
For every Sunday within the look-ahead window:
1.  **Existence Check:** Verify if an `event_instances` record already exists for the `{target_sunday}`.
2.  **Instance Creation:** If absent, initialize a new `event_instances` row linked to the **Sunday Template**.
3.  **Slot Seeding:** Automatically generate three `service_slots` for each new instance:
    *   **1st Slot:** 10:00–12:00 (Target: 15)
    *   **2nd Slot:** 13:00–15:00 (Target: 15)
    *   **3rd Slot:** 16:00–18:00 (Target: 15)
4.  **External Sync:** Trigger a `POST` to the Google Calendar API to mirror the instance.

### **Midweek Prayer (Weekly Wednesday)**
For every Wednesday within the look-ahead window:
1.  **Existence Check:** Verify `event_instances` for `{target_wednesday}`.
2.  **Instance Creation:** Initialize a new `event_instances` row (Type: `MIDWEEK`).
3.  **Structure Note:** Midweek events do not utilize sub-slots; users register for the parent instance directly.
4.  **External Sync:** Trigger a `POST` to the Google Calendar API.

---

## 3. Operational Rules & Constraints

### **Idempotency (Anti-Duplication)**
*   The generator must never overwrite or duplicate an existing date. This allows Admins to manually pre-configure "Special Sundays" (e.g., Anniversary Services) without automated interference.

### **Preservation of Manual Overrides**
*   If an Admin manually adjusts `start_time` or `target_count` for a generated slot, the background worker must **not** revert these changes during its next run.
*   Any manual update in the application must trigger a corresponding `PATCH` request to the Google Calendar API.

### **Special Events Handling**
*   **Manual Entry Only:** Special Events are excluded from automatic generation. They must be created via the Admin Portal to enforce unique capacity limits.
*   **Unidirectional Flow:** Events created directly in the Google Calendar UI (bypassing the app) are ignored by the system and will not appear for registration.

---

## 4. Lifecycle & Cleanup
*   **Archive Policy:** Event data older than **1 year** is flagged for archival to maintain database performance while preserving historical reliability metrics.
*   **Cancellations:** If an event is cancelled within the app, the DB state is updated to `CANCELLED`, and the corresponding Google Calendar entry is removed or renamed to reflect the change.
