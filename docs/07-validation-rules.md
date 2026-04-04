# 07. Validation Rules & System Logic
> **File:** `07-validation-rules.md`  
> **Status:** `STABLE` | **Domain:** `Business Logic & Data Integrity`

---

## 1. User Eligibility & Access
*   **Active Status:** Only users with `status: ACTIVE` (Members) or a verified **Phone + PIN** session (Volunteers) can create or modify registrations.
*   **Restricted Access:** Users with `PENDING` or `DISABLED` status may view the dashboard, but the server must reject all `Register`, `Edit`, and `Move` requests.
*   **Tenure Tracking:** The `service_start_date` is a mandatory field for `USHER` profiles during initial setup. This field is omitted for `VOLUNTEER` profiles to maintain guest simplicity.

---

## 2. Timing & Lockout Logic
*   **The 24-Hour Rule:** Modification and Withdrawal actions are strictly locked exactly 24 hours prior to the `service_slot.start_time`.
    *   **Logic:** `now() < (slot_start_time - 24 hours)`.
*   **The Sunday Rule (The Grace Window):** A Sunday slot is only selectable if the user's committed arrival time is within the allowed window.
    *   **Formula:** `arrival_time <= (slot_start_time + 30 minutes)`.
    *   **Example:** If an Usher arrives at 10:31 AM, the 1st Slot (10:00 AM) is disabled. Slots 2 and 3 remain available.
*   **Minimum Commitment:** A Sunday registration is considered invalid unless it contains at least **one** associated slot.

---

## 3. Capacity & Availability
*   **Special Events:** If a `capacity_limit` is defined (non-NULL), the system must perform a server-side check: `current_count < capacity_limit` before accepting a registration.
*   **Sunday Targets:** The `target_count` (Default: 15) serves as a visual operational guideline. It does **not** hard-block registration unless a manual `capacity_limit` is explicitly applied by an Admin.

---

## 4. Movement & Modification Policy
*   **Clean Slate Movement:** Moving a registration to a new `event_instance_id` (a different date) automatically purges all existing `registration_slots`.
*   **Re-Validation:** Every "Move" action triggers a complete re-run of the "Sunday Rule" and "Lockout Rule" against the target date and time.

---

## 5. Volunteer Security (PIN-Based)
*   **Identification:** Volunteers must provide a **4-digit numeric PIN** upon initial registration.
*   **Authorization:** Any `PATCH` or `DELETE` request targeting a volunteer registration requires the hashed PIN in the payload or a valid Phone-JWT session.

---

## 6. Administrative Overrides
*   **Lockout Bypass:** `CORE_LEADER` and `ADMIN` roles are exempt from the 24-hour lockout and can modify registrations at any time.
*   **State Control:** 
    *   **Ushers/Volunteers:** Limited to toggling between `REGISTERED` and `CANCELLED`.
    *   **Leaders:** Authorized to transition states to `PRESENT`, `ABSENT`, or `EXCUSED`.
*   **Data Correction:** Only Leaders/Admins can modify a `service_start_date` after the initial profile creation to ensure tenure accuracy for legacy members.

---

## 7. Data Integrity Constraints
*   **Temporal Logic:** The `service_start_date` and `birthday` fields must be `date <= current_date`. Future dates return a `422 Unprocessable Entity`.
*   **Role Consistency:** `VOLUNTEER` profiles cannot possess a `service_start_date`. Upon promotion to `USHER`, the Admin must manually initialize this date during the account-linking process.
