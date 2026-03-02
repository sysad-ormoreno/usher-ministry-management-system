# Volunteer Management (MVP)

## Goals
- Allow volunteers (no Google account) to register and later edit/withdraw.
- Avoid requiring full user accounts.
- Keep security simple but adequate for ministry use.

## Authentication Method (MVP)
- Volunteer provides phone number during registration.
- System generates a 6-digit PIN.
- PIN is displayed once on the confirmation screen.
- System stores only a hashed PIN.
- Volunteer uses (phone + PIN) to start a short session to manage registrations.

## Allowed Actions
- Edit registration within the same event instance:
  - Update commitment time
  - Update Sunday slot selections (if event type is SUNDAY)
- Withdraw registration

## Disallowed Actions
- Move registration to a different event instance/date

## Security Notes
- PIN is hashed (argon2/bcrypt).
- Session token is short-lived (e.g., 15 minutes).
- Rate limit attempts per phone/IP to reduce guessing.
