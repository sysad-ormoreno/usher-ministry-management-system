# Usher Portal Rebuild (ROG)

A custom-built usher registration + scheduling system for ROG Ushering Ministry.

This project replaces the current Google Sheets-based portal with a proper backend (API + DB) and frontend UI,
supporting Sunday services, midweek prayer meetings, and special events.

## Why this exists
- Fix limitations of the current system (Google Sheets portal constraints)
- Scale for long-term ministry growth (more events, better coordination)
- Portfolio-grade full-stack project (auth, RBAC, DB schema, APIs, UI, deployment)

## Core Features (MVP)
- Upcoming view grouped by date: **Event name + Day + MMM dd**
- Register / edit / withdraw registrations
- Sunday service: 3 slots (10–12, 1–3, 4–6) with commitment-time eligibility rule (+30 min grace)
- Midweek prayer meeting: weekly instances (Wednesday fixed time)
- Special events: capacity-based registrations (food allocation)
- Core leader mode: view roster (names) + assign aisle leader
- Regular ushers: see counts + targets/capacity, **no names**
- In-app notifications (assigned as aisle leader, reminders)

## Roles & Status
- Roles: ADMIN, CORE_LEADER, USHER
- Status (authoritative): ACTIVE, PENDING, INACTIVE, DISABLED
  - Only ACTIVE users can login/register.

## Key Sunday Rule
A Sunday slot is selectable if:
`commitment_time <= slot_start + 30 minutes`

Examples:
- 12:00 → can choose 2nd & 3rd, not 1st
- 13:30 → can still choose 2nd
- 13:31 → cannot choose 2nd, can choose 3rd

## Targets
Sunday has no hard capacity, but each slot has an ideal target:
- Default: **Ideal = 15** ushers per slot
UI shows: `12 registered (Ideal: 15)`

## Documentation
See `/docs` for specs:
- Product brief
- Roles & permissions
- Wireflow
- Data model
- API spec
- Instance generation logic
- Validation rules
- Roadmap

## Tech Stack (planned)
- Backend: FastAPI (Python)
- DB: PostgreSQL
- Frontend: Next.js (React)
- Auth: Google login + JWT + RBAC
- Deployment: Docker + Nginx + VPS
