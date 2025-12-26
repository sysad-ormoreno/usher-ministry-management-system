# Google Forms → Database Migration Plan

## Phase A: Freeze
- Disable new responses
- Keep data read-only

## Phase B: Audit
- Map form fields to DB fields
- Identify duplicates

## Phase C: Clean
- Normalize names and emails
- Remove test data

## Phase D: Migrate
- Export CSV
- Import using Python scripts
- Log results

## Phase E: Validate
- Compare samples
- Admin sign-off

## Phase F: Decommission
- Archive Forms
- Disable AppSheet
- Document legacy scripts
