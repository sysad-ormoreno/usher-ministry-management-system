# 10-product-logic-burnout.md

## 1. Attendance States & Impact
The `state` of a registration directly impacts the user's **Reliability Score**.
- **PRESENT:** Positive impact.
- **EXCUSED:** Neutral impact (no penalty).
- **CANCELLED (Before Lockout):** Neutral impact.
- **CANCELLED (After Lockout):** Negative impact (Late cancellation).
- **ABSENT:** High negative impact (No-show).

## 2. Reliability Scoring (Rolling 90 Days)
The system calculates a "Reliability %" for each user to help Core Leaders identify who is struggling.
- **Formula:** `(Present + Excused) / (Total Registrations - Early Cancellations)`
- **Thresholds:**
    - **Green (>90%):** Highly Reliable.
    - **Yellow (70-89%):** Needs a check-in.
    - **Red (<70%):** Risk of burnout or disengagement.

## 3. Burnout Monitoring (The "Over-Service" Rule)
To protect the health of the volunteers, the system flags "High Load" users in the Leader Dashboard.
- **Sunday Overload:** If a user is registered for **all 3 slots** in a single Sunday.
- **Consecutive Streak:** If a user has served **4 consecutive Sundays** without a break.
- **Visual Indicator:** These users appear with a **"Flame" icon** next to their name in the Roster View to signal that they should be encouraged to rest.

## 4. The "No-Delete" Audit Logic
Because we never "Hard Delete" a registration:
- **Historical Context:** Even if a volunteer withdraws, the `CANCELLED` record remains linked to their phone number. 
- **Pattern Recognition:** Leaders can see if a volunteer has a pattern of "Last Minute Cancellations," which is often a precursor to total burnout.

## 5. Capacity vs. Target Logic
- **Target (15):** A soft goal. If the count is < 15, the UI shows "Need X more."
- **Capacity (Hard Limit):** Only used for Special Events. If reached, the `Register` button is hard-disabled for all non-admin users.
