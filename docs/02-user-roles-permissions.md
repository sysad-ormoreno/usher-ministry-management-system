# 02-user-roles-permissions.md

## 1. User Status (Account Level)
- **ACTIVE**: Can authenticate and access the dashboard.
- **PENDING**: Can authenticate but only sees "Review in Progress" screen.
- **DISABLED**: Blocked from all system interactions.

## 2. Registration States (Attendance & Health Tracking)
These states track the lifecycle of a specific sign-up for an event.

| State | Meaning |
| :--- | :--- |
| **REGISTERED** | The initial state when an Usher or Volunteer signs up. |
| **PRESENT** | Success state; marked by a Core Leader during or after the service. |
| **ABSENT** | Did not show up with no prior notice (Key indicator for burnout monitoring). |
| **EXCUSED** | User notified a leader they couldn't make it (even within the 24hr lockout). |
| **CANCELLED** | User withdrew their own registration before the 24hr lockout period. |

## 3. Role-Based Access Control (RBAC)

### **Role: USHER**
- **Actions:** View upcoming events, register, and manage own slots.
- **Constraint:** 24-hour lockout applies to `Edit` and `Withdraw` (Change to CANCELLED).
- **Privacy:** Can only see aggregate counts/targets; names of others are hidden.

### **Role: CORE_LEADER**
- **Inheritance:** Includes all **USHER** permissions for their own schedule.
- **Visibility:** Full access to names, phone numbers, and discipler info for all registrants.
- **Management (Exempt from 24hr Lockout):**
    - **Move Registration:** Can shift any user to a different slot or date.
    - **Mark Attendance:** Can update a registration to `PRESENT`, `ABSENT`, or `EXCUSED`.
    - **Aisle Assignment:** Can toggle `is_aisle_leader` for any active registration.
- **Data Integrity:** Encouraged to use `ABSENT/EXCUSED` rather than deleting records to maintain historical data.

### **Role: ADMIN**
- **Inheritance:** Includes all **CORE_LEADER** permissions.
- **Account Management:** Approve `PENDING` users, change Roles, and Disable accounts.
- **System Config:** Define "Ideal Target" numbers and Global Event Templates.

## 4. Volunteer Access (PIN-Based)
- **Auth:** Phone Number + 4-digit Edit PIN.
- **Actions:** Update commitment time or Sunday slot for the specific instance only.
- **Withdrawal:** Can mark themselves as `CANCELLED` (if before the lockout).
