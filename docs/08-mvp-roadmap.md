> **File:** `08-mvp-roadmap.md`  
> **Status:** `STABLE` | **Domain:** `Project Management & Deployment Strategy`

---

## Sprint 0: Foundation & Infrastructure
* **Environment:** FastAPI/PostgreSQL repository initialization and CI/CD pipeline setup.
* **Identity:** Implement Google OAuth2 for Members and JWT logic for Phone+PIN access (Volunteers).
* **RBAC:** Middleware development to enforce `ADMIN`, `CORE_LEADER`, and `USHER` permissions.
* **Calendar API:** Service Account configuration for the Google Calendar "One-Way Mirror" synchronization.

---

## Sprint 1: The Heartbeat (Core Data)
* **Schema:** Execute final table migrations based on `04-data-model.md`.
* **Automation:** Background worker for the 8-week rolling Sunday and Midweek instance generation.
* **Synchronization:** Initial push logic to mirror Database instances to Google Calendar.
* **Audit Engine:** Middleware implementation to capture all state changes into the `audit_log`.

---

## Sprint 2: Registration & Business Logic
* **Sunday Engine:** Implementation of the "Arrival Time vs. Slot Start" (Sunday Rule) validation.
* **Member Flow:** Enable Register, Edit, Move, and Withdraw for Google-authenticated users.
* **Volunteer Flow:** Guest Registration with automated 4-digit PIN generation and validation.
* **Lockout Enforcement:** Backend implementation of the 24-hour precision lockout logic.

---

## Sprint 3: Leadership & Operational Care
* **Roster Visibility:** Privacy-secured interface providing Names, Phones, and Disciplers for Leaders.
* **Attendance Tracking:** UI and API endpoints for marking users as `PRESENT`, `ABSENT`, or `EXCUSED`.
* **The "Undo" Button:** Frontend and Backend logic to revert administrative actions using the Audit Log snapshots.
* **Aisle Leaders:** Assignment logic and initial Push Notification triggers.

---

## Sprint 4: Migration & Go-Live Polish
* **Data Migration:** Scripted import of existing active members and discipler lists from legacy Google Sheets.
* **Service Metrics:** "Need X more" visual indicators and reliability/burnout data views for Leaders.
* **PWA:** Deployment of `manifest.json` and Service Workers for mobile home-screen installation.
* **UX Optimization:** Finalizing global Search and Autocomplete for the Discipler fields.
