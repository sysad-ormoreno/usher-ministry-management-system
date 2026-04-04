# 13. System Configuration & Business Rules

## Overview
This document defines the global variables and logic toggles that govern the Ushering Ministry's automated workflows. These values are stored in the `system_settings` table.

---

## 1. Trainee Verification Rules
These parameters define the threshold for a Trainee to be flagged as "Ready for Review" by a Core Leader.

| Key | Default Value | Description |
| :--- | :--- | :--- |
| `TRAINEE_STREAK_REQUIRED` | `6` | The number of service dates (Sundays) required. |
| `STREAK_MODE` | `STRICT` | The logic used to calculate the streak. |

### Logic Modes:
*   **STRICT**: Requires **consecutive** attendance. If a trainee misses a scheduled Sunday or fails to register, the internal counter resets to zero.
*   **TOTAL**: Requires **cumulative** attendance. The system simply counts the total number of "ATTENDED" statuses within a rolling window (e.g., the last 3 months).

---

## 2. Enrollment Defaults
*   **Auto-Trainee**: All new `VOLUNTEER` registrations are initialized with `is_trainee: True`.
*   **Manual Override**: A Core Leader must manually toggle `is_verified` to `True` once the system flags the user as eligible.
