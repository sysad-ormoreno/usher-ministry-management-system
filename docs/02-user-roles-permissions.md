> **File:** `02-user-roles-permissions.md`  
> **Status:** `STABLE` | **Domain:** `Access Control & Attendance States`

---

## 1. User Status (Account Level)
These statuses govern global access to the application following Google Authentication.

| Status | Description | System Behavior |
| :--- | :--- | :--- |
| **ACTIVE** | Fully verified user. | Access to Dashboard and Registration. |
| **PENDING** | Initial signup state. | Redirected to "Review in Progress" screen. |
| **DISABLED** | Account revoked. | Blocked from all system interactions. |

---

## 2. Registration States
These states track the lifecycle of a specific commitment to an event instance. They are the primary metrics for "Service Health" and burnout monitoring.

* **REGISTERED**: Initial state upon signup.
* **PRESENT**: Confirmed attendance (Marked by Core Leader).
* **ABSENT**: No-show without prior notice; critical for reliability tracking.
* **EXCUSED**: User notified a leader of inability to serve (even within lockout).
* **CANCELLED**: Self-withdrawn by the user *prior* to the 24-hour lockout.

---

## 3. Role-Based Access Control (RBAC)

### **Role: USHER**
* **Scope:** Personal schedule management.
* **Permissions:** View upcoming events, register, and manage own slots.
* **Constraints:** Strict 24-hour lockout for `Edit` and `Withdraw`.
* **Privacy:** Can only view aggregate counts and targets; peer names are hidden.

### **Role: CORE_LEADER**
* **Inheritance:** Includes all **USHER** permissions.
* **Visibility:** Unrestricted access to Names, Phone Numbers, and Discipler info.
* **Management (Exempt from 24hr Lockout):**
    * **Manual Override:** Move any user to a different slot or date.
    * **Attendance Tracking:** Update states to `PRESENT`, `ABSENT`, or `EXCUSED`.
    * **Leadership Assignment:** Toggle `is_aisle_leader` for any registration.

### **Role: ADMIN**
* **Inheritance:** Includes all **CORE_LEADER** permissions.
* **User Governance:** Approve `PENDING` users, manage Roles, and Disable accounts.
* **Global Config:** Define "Ideal Target" numbers and manage Global Event Templates.

---

## 4. Volunteer Access (PIN-Based)
Guest volunteers do not have persistent accounts but manage their records via:
* **Authentication:** Unique Phone Number + 4-digit Edit PIN.
* **Actions:** Update commitment time or Sunday slot for the specific instance only.
* **Withdrawal:** Can self-mark as `CANCELLED` if the 24-hour lockout has not yet triggered.
