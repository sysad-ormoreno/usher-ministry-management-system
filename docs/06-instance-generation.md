# Instance Generation (Sunday + Midweek)

## Goal
Keep future events available for registration (default: next 8–12 weeks).

## Sunday (weekly)
For each upcoming Sunday date:
- Create event_instances row (type=SUNDAY)
- Create 3 service_slots rows:
  - FIRST 10:00–12:00 target=15
  - SECOND 13:00–15:00 target=15
  - THIRD 16:00–18:00 target=15

## Midweek (weekly Wednesday)
For each upcoming Wednesday date:
- Create event_instances row (type=MIDWEEK)
- No slots

## Rules
- Do not duplicate existing instances
- Allow one-off edits per date without breaking future generation
