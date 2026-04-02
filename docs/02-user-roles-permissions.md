# 02-user-roles-permissions.md

## 1. User Status (Account Level)
- **ACTIVE**: Can authenticate and access the dashboard.
- **PENDING**: Can authenticate but only sees "Review in Progress" screen.
- **DISABLED**: Blocked from all system interactions.

## 2. Role-Based Access Control (RBAC)

### **Role: USHER**
- **Actions:** View events, register, edit/withdraw own slots.
- **Constraint:** Lockout applies 24 hours before event start.
- **Visibility:** No access to other members' names/contacts.

### **Role: CORE_LEADER**
- **Inheritance:** Includes all **USHER** permissions for their own schedule.
- **Visibility:** Full access to names, phone numbers, and discipler info for all registrants.
- **Management (Exempt from 24hr Lockout):**
    - **Move Registration:** Can shift any user (Usher/Volunteer) to a different slot or date.
    - **Mark Attendance:** Can update a registration status to `PRESENT`, `ABSENT`, or `EXCUSED`.
    - **Aisle Assignment:** Can toggle `is_aisle_leader` for any active registration.
- **Deletion Rule:** Core Leaders should primarily use `ABSENT` or `EXCUSED` status rather than deleting records, to preserve data for burnout monitoring.

### **Role: ADMIN**
- **Inheritance:** Includes all **CORE_LEADER** permissions.
- **Account Mgmt:** Approve `PENDING` users; change Roles; Disable accounts.
- **System Config:** Manage "Ideal Target" numbers and Global Event Templates.

## 3. Volunteer Access (PIN-Based)
- **Auth:** Phone Number + 4-digit Edit PIN.
- **Actions:** Update commitment time or Sunday slot for the specific instance only.
- **Withdrawal:** Can mark themselves as `CANCELLED` (if before lockout).
