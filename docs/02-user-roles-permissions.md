# 02-user-roles-permissions.md

## 1. User Status (The Global Gatekeeper)
| Status | Authentication | API Access |
| :--- | :--- | :--- |
| **ACTIVE** | Allowed | Full access based on Role. |
| **PENDING** | Allowed | Restricted to "Waiting Room" view only. |
| **INACTIVE/DISABLED** | Denied | No access; redirected to "Account Disabled" page. |

## 2. Role-Based Access Control (RBAC)

### **Role: USHER**
- **Read:** Upcoming events (Dates, Slots, Ideal Targets, Current Counts).
- **Write:** Create/Edit/Withdraw own registrations (subject to 24hr lockout).
- **Profile:** View/Update own basic profile details (Discipler, preferred schedule).
- **Restrictions:** **CANNOT** see names or contact info of other ushers.

### **Role: CORE_LEADER**
- **Inheritance:** Includes all **USHER** permissions.
- **Read:** Full Roster (Names, Phone Numbers, Discipler names) for all events.
- **Write:** Assign/Unassign "Aisle Leader" status to any registered Usher.
- **Special:** View "Volunteer" details to follow up on newcomers.

### **Role: ADMIN**
- **Inheritance:** Includes all **CORE_LEADER** permissions.
- **Write:** Change User Status (e.g., PENDING -> ACTIVE).
- **Write:** Promote/Demote Roles (e.g., USHER -> CORE_LEADER).
- **System:** Define "Ideal Targets" per service slot.

---

## 3. The Volunteer Exception (Non-Authenticated)
Volunteers interact with a separate set of "Public" endpoints.
- **Identity:** Verified via `Phone Number` + `Edit PIN`.
- **Allowed Actions:**
    - Register for a specific event.
    - Update `commitment_time` or `Sunday slot` for that specific instance.
    - Cancel (Withdraw) their registration.
- **Locked Actions:**
    - Cannot "Move" to a different date (must cancel and re-register).
    - Cannot access any Usher-only dashboard or counts.
