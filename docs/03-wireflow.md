# 03. Wireflow & MVP User Experience
> **File:** `03-wireflow.md`  
> **Status:** `STABLE` | **Domain:** `UI/UX Logic & Feature Mapping`

---

## 1. Entry Points & Authentication
*   **Landing Page (Mobile-First):**
    *   **Primary:** `Login with Google` (Ushers/Leaders).
    *   **Secondary:** `Volunteer Registration` (Guest/Provincial users).
    *   **Management:** `Volunteer? Manage your registration` (Phone + PIN access).
*   **The Logic Bridge (Google Users):**
    1. Authenticate via Google OAuth.
    2. **New User:** Redirect to **Profile Setup Form** (Name, Phone, Birthday, Discipler, and **Date Joined Usher Ministry**).
    3. **Existing User:** Redirect to **Dashboard**.
*   **The Waiting Room:** Users with `status: PENDING` are restricted to a "Review in Progress" screen with access to the **Info Tab** (Manuals/Infographics).

---

## 2. Dashboard: Upcoming (Main View)
*   **Navigation:** Chips for `All`, `Sunday`, `Midweek`, and `Special`. Range selectors for `2/4/8 weeks`.
*   **Event Cards:** Grouped by Date. Includes Title, Time, and Status Badge (`REGISTERED`, `PRESENT`, etc.).
*   **Metrics Visibility:**
    *   **Ushers:** See aggregate counts (e.g., "12 registered / Ideal: 15").
    *   **Leaders:** Toggle button to reveal the **Roster Names**.
*   **Primary Actions:** `Register`, `Edit`, or `Withdraw` (Subject to 24hr lockout).

---

## 3. Registration Logic
*   **Discipler Input:** All forms utilize **Autocomplete** based on existing database strings to ensure data cleanliness.
*   **Sunday Service Constraints:**
    *   **Input:** Arrival Time (Time Picker).
    *   **Validation:** Slot checkboxes (1st/2nd/3rd) are disabled if `Arrival Time > Slot Start + 30m`.
*   **Special Events:** The `Register` button is hard-disabled if `current_count >= capacity`.

---

## 4. Volunteer Guest Flow (No Login)
*   **Registration:** Requires Name, Phone, and Discipler. (Service Start Date is excluded for Guests).
*   **Security:** System generates a **4-digit Edit PIN** post-registration.
*   **Management Portal:**
    1. Access via `Phone` + `PIN`.
    2. **Edit:** Update Commitment Time/Slot (Internal to the same instance).
    3. **Withdraw:** Status changed to `CANCELLED` (Soft delete to preserve reliability history).

---

## 5. Core Leader: Management View
*   **Roster Table:** Tabbed by Slot. Displays Name, Role, Phone, and Discipler.
*   **Leadership Actions:**
    *   **Aisle Leader:** Toggle switch for duty assignment.
    *   **Attendance:** One-tap buttons for `PRESENT`, `ABSENT`, or `EXCUSED`.
    *   **Manual Override:** `Move` button to shift users across slots/dates (Bypasses lockout).
*   **Quick Edit Modal:** Click any name to correct typos or update Phone/Discipler.
    *   **Tenure Adjustment:** `Service Start Date` is editable only for `USHER` roles.
    *   **Logging:** Every administrative change triggers an **Audit Log** entry.

---

## 6. Notifications & Alerts
*   **Interface:** Header Bell Icon with unread badge count.
*   **Triggers:**
    *   Aisle Leader duty assignments.
    *   Automated reminders sent exactly before the 24-hour lockout window opens.
*   **Deep-Linking:** Notifications link directly to the specific Event or Sunday Slot page.

---

## 7. Admin: User Directory
*   **Universal Search:** Query by Name, Phone, or Discipler.
*   **Tenure & Milestones:**
    *   **Filters:** Identify users approaching 3, 5, or 10-year anniversaries.
    *   **Badging:** Visual Bronze/Silver/Gold icons for milestone achievers.
*   **Advanced Tools:**
    *   **Manual Tenure Control:** Admin-only override for `service_start_date` for legacy data cleanup.
    *   **Account Linking:** Merge a Volunteer's phone-based history into a new Google-linked profile.
    *   **Status Control:** Global toggle for `ACTIVE`, `PENDING`, or `DISABLED`.
