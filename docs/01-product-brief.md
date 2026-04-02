# 01-product-brief.md: Usher Portal Rebuild (ROG)

## Primary Users
- **Regular Usher** (logged in)
- **Core Leader** (logged in)
- **Volunteer** (no login; registration only)
- **Admin** (logged in)

## Event Types
1) **Sunday Service** (weekly) — 3 slots:
   - 1st: 10:00–12:00
   - 2nd: 13:00–15:00
   - 3rd: 16:00–18:00
   - Default ideal target: 15 per slot

2) **Midweek Prayer Meeting** (weekly, Wednesday) — fixed time

3) **Special Events** (ad hoc) — fixed time, capacity enforced

## Key Workflows
### Usher
- View upcoming events grouped by date.
- Register (can register multiple future dates).
- Edit registration (including moving to another date/event).
- Withdraw registration (subject to the 24-hour lockout rule).

### Core Leader
- View full roster (names + volunteer contact info).
- Assign aisle leader per Sunday slot or special event.
- See counts vs targets/capacity.

### Volunteer
- Register without login using: Full Name, Phone Number, Discipler, and Commitment Time.
- **Identity Logic:** The system uses the Phone Number as a unique identifier to track repeated volunteer activity without requiring a Google account.
- **Limited Access:** Volunteers cannot edit or withdraw their own entries via the portal; manual intervention by a Core Leader or Admin is required for changes.

### Admin
- Approve pending members (status change to ACTIVE).
- Manage core leaders.
- Configure schedule defaults (future).

## Constraints & Rules
### Privacy
- **Regular Ushers:** Restricted to seeing aggregate counts and targets; individual names or contact details are hidden to maintain privacy.
- **Core Leaders:** Full visibility of roster names and contact details for operational management and coordination.

### Timing & Eligibility
- **The Sunday Rule:** A slot is only selectable if the user's `commitment_time` is less than or equal to `slot_start + 30 minutes`.
- **Lockout Period:** Edit and Withdraw functions are disabled for all users 24 hours prior to the event start time to ensure stable planning.

### Authentication
- **Authoritative Status:** Only users with an `ACTIVE` status in the database can log in. `PENDING` or `DISABLED` users are restricted from the dashboard even after Google Auth.

## Communication & Mobile Experience
- **PWA (Progressive Web App):** The portal is built to be "Installed" on mobile home screens, providing a full-screen, native-app feel without an app store.
- **Push Notifications:** Uses the Web Push API to send real-time alerts for:
  - **Aisle Leader Assignments:** Notifying an usher when they are given a specific duty.
  - **Schedule Reminders:** Automatic prompts sent before the 24-hour lockout window begins.
