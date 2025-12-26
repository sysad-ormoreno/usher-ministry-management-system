# Database Schema

## users
- id (UUID, PK)
- name
- email (unique)
- role (usher, admin)
- birth_date
- is_active
- created_at

## events
- id (UUID, PK)
- title
- event_type (service, event)
- start_datetime
- end_datetime
- location
- created_by
- created_at

## registrations
- id (UUID, PK)
- user_id (FK → users)
- event_id (FK → events)
- role
- status
- created_at
