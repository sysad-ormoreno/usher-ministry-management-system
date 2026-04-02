# 03-wireflow.md (Revised Entry Points)

## 1) Landing Page (The Two Doors)
- **Door A: [Login with Google]**
    - Target: Regular Ushers & Leaders.
    - Result: Access to Personal Dashboard, Notifications, and Serving History.
- **Door B: [Volunteer Registration]**
    - Target: Provincial/Senior Volunteers without Google Accounts.
    - Process: Simple form (Name, Phone, Discipler).
    - Result: Success message + "Edit PIN" displayed. No dashboard access.

## 2) Behind the Scenes (The Database Logic)
- **The Usher:** Linked by `google_id`.
- **The Volunteer:** Linked by `phone_number`.
- **The "Promotion":** If a Volunteer eventually gets a Google account, an **Admin** can "Link" their phone-based history to their new Google profile.

## 3) Core Leader View (The Bridge)
- In the Roster Table, the Leader sees both.
- **Icon 1:** A Google icon next to Ushers (Logged in).
- **Icon 2:** A Phone icon next to Volunteers (Guest).
- **Action:** The Leader can call either one directly from the app.
