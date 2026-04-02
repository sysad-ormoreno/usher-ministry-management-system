# 03-wireflow.md (MVP)

## 1) Entry Points & Auth Flow
- **Primary Action:** [Login with Google]
- **The Logic Bridge:**
    1. User authenticates via Google.
    2. Backend checks `Profiles` table for matching `google_id`.
    3. **IF FOUND:** Redirect to **Dashboard**.
    4. **IF NOT FOUND:** Redirect to **New Member Profile Form**.
- **The New Member Form:**
    - Fields: First/Last Name, Contact Number, Birthday, Discipler, Preferred Schedule.
    - Submit: Status set to `PENDING`. Redirect to **Waiting Room**.

## 2) The Waiting Room (For PENDING status)
- **Message:** "Welcome to the Ministry! A Core Leader is reviewing your profile."
- **Access:** Can only see the **Info Tab** (Infographics/Manuals).
- **Trigger:** Once Admin changes status to `ACTIVE`, the next login/refresh opens the **Dashboard**.

## 3) Dashboard: Upcoming (Main View)
- **Grouping:** Date-based headers (e.g., `Sun, Apr 12`).
- **Cards:** Service/Event type, time, and real-time counts.
- **Interactions:** 
    - `Register` / `Edit` / `Withdraw` (Subject to 24h lockout).
    - Status badges: `REGISTERED`, `PRESENT`, `ABSENT`, `EXCUSED`.

## 4) Core Leader: Management View
- **Roster Table:** Access to all registrant details.
- **Attendance Tools:** 
    - Mark `PRESENT`, `ABSENT`, or `EXCUSED`.
    - Toggle `Aisle Leader`.
    - "Move" registration (Exempt from lockout).

## 5) Volunteer: PIN Management
- **Secondary Entry:** "Volunteer? Manage here" link on Landing Page.
- **Security:** Phone + 4-digit PIN.
- **Limits:** Can only edit/cancel their specific instance; no "Move" to other dates.

## 6) Notifications
- **In-App:** Bell icon with unread indicator.
- **Deep-linking:** Clicking a notification (e.g., "Assigned as Aisle Leader") navigates the user directly to the specific Sunday slot.
