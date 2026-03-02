# API Spec v1 (outline)

## Auth
- POST /auth/login/google
- GET /me

## Events
- GET /events/upcoming?from&to
- GET /events/{id}

## Registrations (User)
- POST /registrations
- PATCH /registrations/{registration_group_id}   # edit + move
- POST /registrations/{registration_group_id}/cancel
- GET /me/registrations?from&to

## Volunteer
- POST /volunteer-registrations

## Core Leader
- GET /events/{id}/roster
- POST /assignments

## Notifications
- GET /me/notifications
- POST /me/notifications/{id}/read
