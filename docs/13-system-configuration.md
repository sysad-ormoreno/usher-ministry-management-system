# 13. System Configuration & Logic
> **File:** `13-system-configuration.md`  
> **Status:** `STABLE` | **Domain:** `Global Settings & Administrative Overrides`

---

## 1. Overview
This document defines the global variables and logic toggles that govern the Ushering Ministry's automated workflows. These values are stored in the `system_settings` table to allow real-time adjustments without code deployments.

---

## 2. Trainee Verification Rules
These parameters define the threshold for a Trainee to be flagged as "Ready for Review" by a Core Leader.

| Key | Default Value | Description |
| :--- | :--- | :--- |
| `TRAINEE_STREAK_REQUIRED` | `6` | The number of service dates (Sundays) required. |
| `STREAK_MODE` | `STRICT` | The logic used to calculate the streak. |

### Logic Modes:
- **STRICT:** Requires **consecutive** attendance. If a trainee misses a scheduled Sunday or fails to register, the internal counter resets to zero.
- **TOTAL:** Requires **cumulative** attendance. The system simply counts the total number of `PRESENT` statuses within a rolling window.

---

## 3. Event Generation Defaults (The "Control Panel")
These values are fetched by the background worker to seed the 8-week rolling schedule every Monday at 00:00.

| Key | Default Value | Description |
| :--- | :--- | :--- |
| `SUN_SLOT_1_TIME` | `10:00-12:00` | Time range for the 1st Sunday Slot. |
| `SUN_SLOT_2_TIME` | `13:00-15:00` | Time range for the 2nd Sunday Slot. |
| `SUN_SLOT_3_TIME` | `16:00-18:00` | Time range for the 3rd Sunday Slot. |
| `SUN_SLOT_TARGET` | `15` | Default target number of ushers per Sunday slot. |
| `MIDWEEK_START_TIME` | `19:00` | Default start time for Wednesday Prayer Meetings. |

---

## 4. Enrollment & State Defaults
- **Auto-Trainee:** All new `VOLUNTEER` registrations are initialized with `is_trainee: True`.
- **Manual Override:** A Core Leader must manually toggle `is_verified` to `True` once the system flags the user as eligible based on the `TRAINEE_STREAK_REQUIRED`.
- **Lockout Bypass:** Only `ADMIN` or `CORE_LEADER` roles can bypass the 24-hour modification lockout via the system's internal override flag.
