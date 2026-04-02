# 03-wireflow.md (Detailed MVP)

## 1) Entry Points & Authentication
- **Landing Page (Mobile-First):**
    - **Primary Button:** `Login with Google` (For Ushers/Leaders).
    - **Secondary Link:** `Volunteer Registration` (For provincial/senior members).
    - **Management Link:** `Volunteer? Manage your registration` (Phone + PIN entry).
- **The Logic Bridge (Google Users):**
    1. Authenticate via Google.
    2. Backend checks `google_id` in `Profiles` table.
    3. **New User:** Redirect to **Profile Setup Form** (First/Last, Phone, Birthday, Discipler).
    4. **Existing User:** Redirect to **Dashboard**.
- **The Waiting Room:** Users with `status: PENDING` see a "Review in Progress" screen with access to the **Info Tab** (Manuals/Infographics).

## 2) Dashboard: Upcoming (Main View)
- **Filters & Navigation:**
    - **Chips:** `All` / `Sunday` / `Midweek` / `Special`.
    - **Range Selector:** `Next 2` / `4` / `8 weeks`.
- **Event List:** Grouped by Date header (e.g., `Sun, Mar 08`).
- **Cards (Usher/Leader View):**
    - **Header:** Event Title + Time Range + Status Badge (`REGISTERED`, `PRESENT`, `ABSENT`, `EXCUSED`, `CANCELLED`).
    - **Usher Metrics:** `12 registered (Ideal: 15)` or `15/20 (Capacity)`.
    - **Leader Metrics:** Toggle button to "View Roster Names."
- **Primary Actions:**
    - `Register` (if spot available and user not already registered).
    - `Edit` / `Withdraw` (if registered & before 24hr lockout).

## 3) Registration Flows
- **Input Logic (Discipler):** All registration forms use an **Autocomplete/Suggestion** field for "Discipler Name" based on existing database entries to prevent duplicate variations.
- **Sunday Service:**
    - **Input:** `Arrival Time` (Time Picker).
    - **Slot Selection:** 1st/2nd/3rd checkboxes.
    - **Logic:** Disable checkboxes where `Arrival Time > Slot Start + 30m`.
    - **Action:** Confirm to POST registration.
- **Midweek Prayer:**
    - **Input:** `Commitment Time` (Required).
    - **Action:** Confirm registration.
- **Special Events:**
    - **Input:** `Commitment Time`.
    - **Logic:** Disable `Register` button if `current_count >= capacity`.
    - **Action:** Confirm registration.

## 4) Volunteer Flow (No Login)
- **Registration:** Same form as Sunday/Midweek but includes mandatory fields for `Full Name`, `Phone`, and `Discipler` (Autocomplete enabled).
- **Post-Registration:** System generates and displays a **4-digit Edit PIN**. Instructions provided to save for future management.
- **Management:** 
    1. Enter `Phone Number` + `PIN`.
    2. View list of active registrations for that specific phone.
    3. **Edit:** Update `Commitment Time` or `Slot` (Restricted to the same day/instance).
    4. **Withdraw:** Mark registration as `CANCELLED`. **Note:** Records are never deleted; status is changed to preserve reliability history.

## 5) Core Leader: Management View
- **Event Detail Page:**
    - **Sunday View:** Tabbed navigation for 1st, 2nd, and 3rd slots.
    - **Roster Table:** Display Full Name, Role Badge, Phone, and Discipler.
- **Management Actions:**
    - **Aisle Leader:** Toggle switch to assign/unassign the "Aisle Leader" duty.
    - **Attendance Tracking:** Action buttons to update state to `PRESENT`, `ABSENT`, or `EXCUSED`.
    - **Override Management:** `Move` button to manually shift a user to a different slot or date. 
    - **Profile Correction:** Ability to click **any** user's name (Usher or Volunteer) to open a **Quick Edit Modal**.
        - **Editable Fields:** First Name, Last Name, Phone, and Discipler Name.
        - **Audit Trail:** The system must log: *"Admin [Name] updated Profile [ID] Name from 'Jhon' to 'John'"*.

## 6) Notifications
- **Interface:** Bell icon in the app header with a red unread count badge.
- **Content:**
    - Duty assignments (e.g., "Assigned as Aisle Leader for 2nd Slot").
    - Automated reminders (e.g., "24 hours until Sunday Service - Last chance to edit").
- **Interaction:** Clicking a notification item deep-links the user directly to the relevant Event Detail or Sunday Slot page.

## 7) Admin: User Directory (Cleanup)
- **Access:** Restricted to `ADMIN` and `CORE_LEADER` roles.
- **Search:** Global search by Name, Phone, or Discipler.
- **Unified Profile Management:**
    - **Edit All Profiles:** Centralized interface to correct typos for the entire database (both Google-linked Ushers and PIN-based Volunteers).
    - **Account Linking:** If a Volunteer later signs in with Google, Admins use this view to merge the "Volunteer Profile" into the new "Google Profile" to keep their service history intact.
    - **Status Control:** Toggle `ACTIVE`, `PENDING`, or `DISABLED` for any user.
