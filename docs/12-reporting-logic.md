# 12. Reporting Logic & Recognition
> **File:** `12-reporting-logic.md`  
> **Status:** `STABLE` | **Domain:** `Community Building & Service Milestones`

---

## 1. Birthday Dashboard
**Objective:** Provide Core Leaders with a monthly overview of usher birthdays for community building.
- **Privacy Rule:** The API must hide the birth year. Only Month and Day are exposed to the frontend.
- **Aggregation:** Data must be grouped by month with a count of total birthdays per month.
- **Visual Goal:** A calendar or list view highlighting "Birthdays This Month" for easier fellowship planning.

---

## 2. Tenure & Recognition Audit
**Objective:** Identify ushers eligible for service awards (3, 5, 10, 15, 20 years).
- **Precision:** Calculations must use 365.25 days to account for leap years.
- **Status Flags:**
    - `OVERDUE`: Usher has passed a milestone but hasn't been flagged for recognition yet.
    - `ON TRACK`: Usher is approaching their next milestone.
- **Countdown:** Provide a "Days Until" value for upcoming anniversaries.
- **Data Source:** Pulls directly from `service_start_date` defined in the `user_profiles` table.

---

## 3. Reliability & Burnout Analytics
**Objective:** Aggregate historical data to assess the health of the volunteer pool.
- **Rolling Metrics:** Calculate Reliability % based on the last 90 days of activity.
- **High-Load Flags:** Identify users serving 4+ consecutive weeks or 3 slots in a single Sunday.
- **Late Cancellation Trends:** Track the frequency of state changes from `REGISTERED` to `CANCELLED` within the 24-hour lockout window (Admin-only view).
