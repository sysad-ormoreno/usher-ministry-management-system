# 03-wireflow.md (MVP)

## 1) Entry Points & Auth
- **Public Landing:** 
    - "Login with Google" (Ushers/Leaders)
    - "New Member Registration" (Custom Form)
    - "Volunteer Registration" (Custom Form)
    - "Manage Volunteer Registration" (Phone + PIN entry)
- **The Waiting Room:** (For `PENDING` status)
    - Message: "Your application is under review by the Core Leaders."
    - Links to the "Info" tab (Infographics).

## 2) Dashboard: Upcoming (Main View)
- **Header:** Grouped by Date (e.g., `Sun, Apr 12`).
- **Cards:** `Sunday Service`, `Midweek`, `Special Events`.
- **Metrics:** 
    - `12/15 Registered` (Ushers see counts).
    - `[Name List]` (Core Leaders see names).
- **Actions:** 
    - `Register` button (if available).
    - `Edit / Withdraw` (subject to 24hr lockout).
- **Filters:** Type (Sunday/Midweek) and Date Range.

## 3) The Registration Flow
- **Sunday:** 
    - Input: `Arrival Time`.
    - Logic: Checkboxes for 1st/2nd/3rd slots only enabled if `Arrival Time <= Slot Start + 30m`.
- **Midweek/Special:** 
    - Input: `Commitment Time`.
    - Logic: Check against Capacity (for Special Events).

## 4) Core Leader: Management View
- **Roster Table:** Full names, Phone (for volunteers), Discipler.
- **Attendance Actions:** 
    - Toggle: `PRESENT` / `ABSENT` / `EXCUSED`.
    - Toggle: `AISLE LEADER` status.
- **Override:** "Move" user to a different slot (Exempt from 24hr lockout).

## 5) Volunteer: PIN Management
- **Flow:** 
    1. Enter Phone + PIN.
    2. List of active registrations for that phone number.
    3. Edit `Commitment Time` or `Slot` (same day only).
    4. Withdraw (Cancel).

## 6) Notifications
- **Bell Icon:** Shows unread count.
- **List:** "You were assigned as Aisle Leader for 2nd Slot," "Reminder: 24hrs until Sunday Service."
- **Interaction:** Clicking an item navigates directly to that Event/Slot.
