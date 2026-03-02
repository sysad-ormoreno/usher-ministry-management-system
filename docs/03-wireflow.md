# Wireflow (MVP)

## 1) Dashboard: Upcoming
- Grouped by date header: `Sun, Mar 08`
- Each item shows:
  - Title: `Sunday Service`, `Midweek Prayer Meeting`, `Encounter Night`
  - Time range
  - Counts:
    - Sunday slots: `12 registered (Ideal: 15)`
    - Special: `15 registered (Capacity: 20)`
- Actions:
  - Register (if not registered)
  - Edit / Withdraw (if registered)

Filters:
- Chips: All / Sunday / Midweek / Special
- Range: Next 2 / 4 / 8 weeks

## 2) Register: Sunday
- Select commitment time (time picker)
- Select slot(s): 1st/2nd/3rd (checkboxes)
- Disable slots that fail eligibility rule
- Confirm

## 3) Register: Midweek
- Confirm registration (commitment time optional or required — v1 can require)

## 4) Register: Special
- Confirm registration with commitment time
- Enforce capacity

## 5) Edit Registration
- Change commitment time
- Change selected slots (if Sunday)
- Move to another date/event instance
- Withdraw

## 6) Core Leader: Event Detail + Roster
- For Sunday: tabs per slot (1st/2nd/3rd)
- Table shows names (and volunteer phone/discipler)
- Button to assign aisle leader

## 7) Notifications
- In-app list + bell badge count
- Click notification deep-links to event detail

## Volunteer: Manage Registration (no login)
Entry point:
- Button/link: "Volunteer? Manage your registration"

Flow:
1) Enter phone number + PIN
2) View upcoming registrations for that phone
3) Edit (commitment time + slots if Sunday) or Withdraw
4) No "Move" option for volunteers
