# Product Brief (MVP)

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
- View upcoming events grouped by date
- Register (can register multiple future dates)
- Edit registration (including moving to another date/event)
- Withdraw registration (subject to the 24-hour lockout rule)

### Core Leader
- View full roster (names + volunteer contact info)
- Assign aisle leader per Sunday slot or special event
- See counts vs targets/capacity

### Volunteer
- Register without login using: Full Name, Phone Number, Discipler, and Commitment Time
- **Identity Logic:** The system uses the Phone Number as a unique identifier to track repeated volunteer activity without requiring a Google account.
- **Limited Access:** Volunteers cannot edit or withdraw their own entries via the portal; manual intervention by a Core Leader or Admin is required for changes.

### Admin
- Approve pending members (status change to ACTIVE)
- Manage core leaders
- Configure schedule defaults (future)

## Constraints & Rules
### Privacy
- **Regular Ushers:** Can see aggregate counts/targets/capacity but are restricted from seeing individual names or contact details.
- **Core Leaders:** Full visibility of roster names and contact details for operational management.

### Timing & Eligibility
- **The Sunday Rule:** A slot is only selectable if the user's `commitment_time` is less than or equal to `slot_start + 30 minutes`. (e.g., A 1:35 PM arrival is ineligible for the 1:00 PM slot).
- **Lockout Period:** Edit and Withdraw functions are disabled for all users 24 hours prior to the event start time to ensure stable planning for leaders.

### Authentication
- **Authoritative Status:** Only users with an `ACTIVE` status in the database can successfully log in and interact with protected features. `PENDING` or `DISABLED` users are restricted from the dashboard.

## Communication & Experience (PWA)
- **Mobile-First Design:** The portal is a Progressive Web App (PWA), allowing ushers to "Install" it to their mobile home screens for a native-app experience.
- **In-App Notifications:** - **Aisle Leader Alerts:** Real-time notification when a Core Leader assigns a specific duty.
  - **Schedule Reminders:** Automatic "check-in" prompts sent prior to the 24-hour lockout window.
- **Push Notifications:** Leverages the Web Push API to send alerts directly to the user's device lock screen (requires user permission).
