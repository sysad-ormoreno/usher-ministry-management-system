# Reporting & Leader Dashboards

## 1. Birthday Dashboard
**Objective:** Provide Core Leaders with a monthly overview of usher birthdays for community building.
- **Privacy Rule:** The API must hide the birth year. Only Month and Day are exposed to the frontend.
- **Aggregation:** Data must be grouped by month with a count of total birthdays per month.

## 2. Tenure & Recognition Audit
**Objective:** Identify ushers eligible for service awards (3, 5, 10, 15, 20 years).
- **Precision:** Calculations must use 365.25 days to account for leap years.
- **Status Flags:** - `OVERDUE`: Usher has passed a milestone but hasn't been flagged for recognition yet.
    - `ON TRACK`: Usher is approaching their next milestone.
- **Countdown:** Provide a "Days Until" value for upcoming anniversaries.
