# 01-product-brief.md: Usher Portal Rebuild (ROG)

## Primary Users
- **Regular Usher** (logged in via Google)
- **Core Leader** (logged in via Google)
- **Volunteer** (no login; phone-based registration)
- **Admin** (logged in via Google)

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
- **Register:** Can sign up for multiple future dates/slots.
- **Move Registration:** Changing a registration date affects the **entire day's commitment** (the parent Event Instance). If an Usher moves from one Sunday to another, all slot selections for the original day are cleared, and they must select slots for the new date.
- **Withdraw Registration:** Subject to the precise 24-hour lockout rule.

### Core Leader
- **Full Roster:** View names, volunteer contact info, and discipler.
- **Attendance & Management:** Mark users as `PRESENT`, `ABSENT`, or `EXCUSED`.
- **Assignment:** Assign "Aisle Leader" per Sunday slot or special event.
- **Override:** Can Move or Edit any registration regardless of the 24-hour lockout.

### Volunteer (Guest)
- **Registration:** Uses Full Name, Phone Number, Discipler (with Autocomplete), and Commitment Time.
- **Identity Logic:** Phone Number serves as the unique identifier.
- **Self-Management:** Can Edit or Withdraw their own entry using a **4-digit PIN** provided at registration. 
- **No Deletion:** When a Volunteer withdraws, the record is marked as `CANCELLED` in the database to preserve reliability data (no hard deletes).

### Admin
- **User Management:** Approve `PENDING` members to `ACTIVE`.
- **Role Management:** Promote/Demote Core Leaders.
- **System Config:** Manage event templates and ideal targets.

## Constraints & Rules
### Privacy & Data Integrity
- **Regular Ushers:** See aggregate counts and targets only.
- **Core Leaders:** Full visibility for operational coordination.
- **Discipler Entry:** To maintain data cleanliness, the UI provides an **Autocomplete/Suggestion** list based on existing names in the database to prevent duplicate variations (e.g., "Pst. John" vs "Pastor John").

### Timing & Eligibility
- **The Sunday Rule:** A slot is only selectable if the user's `commitment_time` is less than or equal to `slot_start + 30 minutes`.
- **Precision Lockout:** The 24-hour lockout period is calculated relative to the **specific `service_slot.start_time`**. 
  - *Example:* If the 1st slot starts at 10:00 AM Sunday, the lockout for that slot begins at 10:00 AM Saturday.
- **Movement Constraint:** Moving a registration to a new date is treated as a fresh registration for that new day; previous slot data does not "carry over" to ensure slot availability is re-validated.

### Authentication
- **Authoritative Status:** Only `ACTIVE` users can access the dashboard. `PENDING` or `DISABLED` users are redirected to a "Waiting Room" or "Contact Admin" screen after Google Auth.

## Communication & Mobile Experience
- **PWA (Progressive Web App):** Optimized for home-screen installation.
- **Push Notifications:** Real-time alerts for Aisle Leader assignments and reminders sent exactly before the 24-hour lockout window opens.
