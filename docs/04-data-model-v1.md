# Data Model v1

## Entities
- users (role + status)
- user_profiles (phone, discipler, start_date, training, etc.)
- event_instances (SUNDAY/MIDWEEK/SPECIAL)
- service_slots (Sunday only; includes target_count default 15)
- registration_groups (one per user/volunteer per event instance)
- registration_group_slots (many-to-many, Sunday selected slots)
- assignments (AISLE_LEADER)
- notifications
- audit_log (recommended)

## Special Notes
- Special events: register per event instance (no slots)
- Midweek: weekly instances generated ahead
- Sunday: weekly instances generated ahead + 3 slots
- Regular ushers see counts/targets/capacity only
