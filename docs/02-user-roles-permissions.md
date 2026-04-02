# 02-user-roles-permissions.md

## 1. User Status (The Global Gatekeeper)
| Status | Authentication | API Access |
| :--- | :--- | :--- |
| **ACTIVE** | Allowed | Full access based on Role. |
| **PENDING** | Allowed | Restricted to "Waiting Room" (Review Status) view. |
| **INACTIVE/DISABLED** | Denied | Hard block; Redirected to "Contact Admin" page. |

## 2. Role-Based Access Control (RBAC)

### **Role: USHER**
- **Read:** Upcoming events (Dates, Slots, Ideal Targets, Current Counts).
- **Write:** Create/Edit/Withdraw **own** registrations.
- **Constraint:** Subject to the **24-hour lockout** rule.
- **Privacy:** Restricted from seeing names/contacts of others.

### **Role: CORE_LEADER**
- **Inheritance:** Includes all **USHER** permissions (for their own serving slots).
- **Read:** Full Roster (Names, Phone Numbers, Discipler) for all events.
- **Write (Override):** Can Edit, Move, or Withdraw **any** registration (Usher, Volunteer, or fellow Core Leader).
- **Constraint:** **Exempt** from the 24-hour lockout rule (can manage roster in real-time).
- **Write:** Assign/Unassign "Aisle Leader" status.

### **Role: ADMIN**
- **Inheritance:** Includes all **CORE_LEADER** permissions.
- **Write:** System-wide User Management (Change Status: PENDING -> ACTIVE).
- **Write:** Role Management (Promote/Demote users).
- **Config:** Set "Ideal Targets" and Event Templates.

---

## 3. Volunteer Access (PIN-Based)
- **Validation:** Phone Number + Edit PIN.
- **Write:** Update commitment time/slot for the **current registered instance only**.
- **Constraint:** Cannot move to a different date. Cannot see any "Usher" dashboards.
