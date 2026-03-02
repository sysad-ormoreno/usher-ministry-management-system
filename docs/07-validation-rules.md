# Validation Rules

## Status
Only ACTIVE users can register/edit/move.

## Sunday slot eligibility
A slot is selectable if:
commitment_time <= slot_start + 30 minutes

If commitment_time is 13:31:
- cannot select 2nd service (13:00 start)
- can select 3rd service (16:00 start)

## Sunday minimum
Must select at least 1 slot.

## Special event capacity
If capacity is set:
registered_count < capacity
Otherwise reject as FULL.

## Moving registrations
PATCH can change event_instance_id.
Re-validate based on new target event.
