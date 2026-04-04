# 01. Product Brief: Usher Portal Rebuild (ROG)
> **File:** `01-product-brief.md`  
> **Status:** `STABLE` | **Domain:** `Product Requirements & Workflows`

---

## 1. Executive Summary
The ROG Usher Portal is a centralized coordination platform designed to manage Sunday Services, Midweek Meetings, and Special Events. It balances the needs of authenticated regular ushers, high-privilege Core Leaders, and unauthenticated guest volunteers through a phone-based identification system.

---

## 2. Primary User Personas
| Role | Access Level | Authentication |
| :--- | :--- | :--- |
| **Regular Usher** | Dashboard / Registration | Google OAuth (Active Status) |
| **Core Leader** | Roster / Attendance / Assignment | Google OAuth (Elevated) |
| **Admin** | System Config / User Approval | Google OAuth (Root) |
| **Volunteer** | Guest Registration | Phone Number + 4-Digit PIN |

---

## 3. Event Architecture
1. **Sunday Service (Weekly)**
   - Slot 1: 10:00–12:00
   - Slot 2: 13:00–15:00
   - Slot 3: 16:00–18:00
   - **Capacity:** Default target of 15 ushers per slot.
2. **Midweek Prayer Meeting (Wednesday)**
   - Fixed time; single slot.
3. **Special Events (Ad Hoc)**
   - Variable times and enforced capacity limits.

---

## 4. Key Workflows

### Usher Workflow
* **Registration:** Sign up for multiple future dates/slots.
* **The "Clean Slate" Move:** Changing a registration date clears all slot selections for the original day. Users must re-select slots for the new date to ensure availability validation.
* **Withdrawal:** Restricted by a precise **24-hour lockout** relative to the specific `service_slot.start_time`.

### Core Leader Workflow
* **Attendance Management:** Tag users as `PRESENT`, `ABSENT`, or `EXCUSED`.
* **Leadership Assignment:** Designate "Aisle Leaders" for specific slots.
* **Administrative Override:** Permission to move or edit any registration, bypassing the 24-hour lockout.

### Volunteer (Guest) Workflow
* **Identification:** Phone Number acts as the Primary Key.
* **Data Integrity:** Discipler entry uses **Autocomplete** to prevent variations (e.g., "Pst. John" vs "Pastor John").
* **Self-Service:** Edit or withdraw entries using a **4-digit PIN**.
* **Soft Deletes:** Withdrawals are marked as `CANCELLED` to preserve reliability metrics; records are never hard-deleted.

---

## 5. Constraints & Business Rules

### Precision Timing
* **The Sunday Rule:** A slot is only selectable if the user's `commitment_time` is $\le$ `slot_start + 30 minutes`.
* **Lockout Logic:** The 24-hour window is calculated per slot. If a slot starts at 10:00 AM Sunday, the lockout triggers at 10:00 AM Saturday.

### Privacy & Visibility
* **Ushers:** Access to aggregate counts and targets only.
* **Leaders:** Full PII (Personally Identifiable Information) access for operational coordination.

### Technical Requirements
* **PWA:** Optimized for mobile home-screen installation.
* **Notifications:** Real-time alerts for Aisle Leader assignments and pre-lockout reminders.
* **Auth Gate:** `PENDING` or `DISABLED` users are restricted to a "Waiting Room" screen post-login.
