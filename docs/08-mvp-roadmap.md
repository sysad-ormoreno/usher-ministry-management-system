# 12-mvp-roadmap.md

## Sprint 0: Foundation & Auth (Infrastructure)
- [ ] **Environment:** FastAPI/PostgreSQL repo setup + CI/CD pipeline.
- [ ] **Identity:** Google OAuth2 (Members) & JWT logic for Phone+PIN (Volunteers).
- [ ] **RBAC:** Middleware to enforce ADMIN, CORE_LEADER, and USHER permissions.
- [ ] **Calendar API:** Service Account setup for Google Calendar "One-Way Mirror" sync.

## Sprint 1: The Heartbeat (Core Data)
- [ ] **Schema:** Implement final tables from `04-data-model`.
- [ ] **Generation:** Background worker for 8-week rolling Sunday/Midweek instances.
- [ ] **Sync:** Initial push logic from DB to Google Calendar.
- [ ] **Audit Engine:** Middleware to capture all state changes into `audit_log`.

## Sprint 2: Registration & Rules (User Experience)
- [ ] **Sunday Engine:** Implementation of "Arrival Time vs. Slot Start" validation.
- [ ] **Member Flow:** Register/Edit/Move/Withdraw for Google-authenticated users.
- [ ] **Volunteer Flow:** Registration + 4-digit PIN generation & validation.
- [ ] **Lockout Enforcement:** 24-hour precision lockout logic.

## Sprint 3: Leadership & Care (Operational Ops)
- [ ] **Roster View:** Privacy-secured list of names, phones, and disciplers for Leaders.
- [ ] **Attendance Tracking:** UI/API for marking Present/Absent/Excused.
- [ ] **The "Undo" Button:** Frontend/Backend logic to revert actions using Audit Logs.
- [ ] **Aisle Leaders:** Assignment logic + Push Notification triggers.

## Sprint 4: Migration & Polish (Go-Live)
- [ ] **Data Seed:** Script to import existing active members/disciplers from Google Sheets.
- [ ] **Metrics:** "Need X more" indicators and burnout/reliability data views.
- [ ] **PWA:** Manifest.json and Service Worker for home-screen installation.
- [ ] **Optimization:** Search/Autocomplete for the Discipler field.
