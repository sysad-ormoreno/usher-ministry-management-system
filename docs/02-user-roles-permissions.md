# Roles & Permissions

## Roles
- ADMIN
- CORE_LEADER
- USHER

## Status (authoritative)
- ACTIVE: can login/register
- PENDING: cannot login/register
- INACTIVE/DISABLED: cannot login/register

## Permissions Matrix (MVP)
### USHER
- View upcoming events/services
- View counts + targets/capacity (no names)
- Create/edit/move/withdraw own registrations
- View own notifications

### CORE_LEADER
- All USHER permissions
- View roster names/details for any event
- Assign aisle leader
- Create/manage special events (optional MVP; can be admin-only if preferred)

### ADMIN
- All CORE_LEADER permissions
- Approve members (PENDING -> ACTIVE)
- Manage roles
- System settings (targets, schedule templates) (phase 2 if not MVP)

### VOLUNTEER (no login)
Volunteers can:
- Register for an event/service (with name, phone, discipler, commitment time)
- Edit their registration **only for the same event instance**
  - Allowed: commitment time, Sunday slot selection (if Sunday)
  - Not allowed: move to another date/event instance
- Withdraw (cancel) their registration

Volunteers authenticate for editing via:
- phone number + edit PIN (shown once at registration time)
