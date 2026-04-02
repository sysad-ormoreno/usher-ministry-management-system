# 06-instance-generation.md

## 1. Goal & Frequency
- **Objective:** Maintain a rolling window of **8–12 weeks** of future events to allow for long-term scheduling.
- **Trigger:** A background worker (Cron Job) runs once every Monday at 00:00.
- **Source of Truth:** The PostgreSQL database is the authoritative source for all events. The external Google Calendar acts as a "One-Way Mirror" for public display.

## 2. Generation Logic

### **Sunday Services (Weekly)**
For every Sunday within the 8-week look-ahead window:
1. **Check Existence:** Look for an `event_instances` record where `date = {target_sunday}` and `type = SUNDAY`.
2. **Instance Creation:** If not found, create a new `event_instances` row linked to the Sunday Template.
3. **Slot Seeding:** For each new instance, automatically generate three `service_slots`:
    - **1st Slot:** 10:00–12:00 (Target: 15)
    - **2nd Slot:** 13:00–15:00 (Target: 15)
    - **3rd Slot:** 16:00–18:00 (Target: 15)
4. **Sync:** Trigger a `POST` to the Google Calendar API to reflect the new instance.

### **Midweek Prayer (Weekly Wednesday)**
For every Wednesday within the 8-week look-ahead window:
1. **Check Existence:** Look for an `event_instances` record where `date = {target_wednesday}` and `type = MIDWEEK`.
2. **Instance Creation:** If not found, create a new `event_instances` row.
3. **Note:** No slots are generated for Midweek; users register for the instance directly.
4. **Sync:** Trigger a `POST` to the Google Calendar API to reflect the new instance.

## 3. Operational Rules

### **Idempotency (Anti-Duplication)**
- The generator must never create a duplicate for a date that already exists. This allows Admins to manually create a "Special Sunday" ahead of time without the generator interfering.

### **Manual Overrides**
- If an Admin manually changes the `start_time` or `target_count` of a specific generated slot, the generator must **not** revert those changes. 
- Updates in the app must trigger a corresponding `PATCH` to the Google Calendar API.

### **Special Events**
- Special Events are **excluded** from automatic generation. They must be created manually via the Admin Portal. Manual creation triggers a Google Calendar sync.
- Events created directly in Google Calendar (bypassing the app) will not be available for registration.

## 4. Cleanup Logic
- **Archive Policy:** Events older than 1 year should be flagged for archival. 
- **Cancellations:** If an event is cancelled in the app, mark it as `CANCELLED` in the DB and remove/rename the entry in Google Calendar.
