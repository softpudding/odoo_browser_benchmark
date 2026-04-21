# Request a half-day (morning) time-off

You are logged in to Odoo 19 as **Administrator** in the **Time Off** app.

You need to request a **half-day** of **Paid Time Off** for the **morning
only** of **June 15, 2026**, because of a doctor's appointment.

## What to do

1. From the **Time Off** app, click **New Time Off** (or the **New** button
   on My Time Off).
2. Fill in the request:
   - **Time Off Type**: `Paid Time Off`
   - The form should show a **Half Day** / Morning/Afternoon selector
     (the leave type is configured for half-day requests).
   - **Date**: `June 15, 2026`
   - **Morning/Afternoon**: `Morning`
   - **Description**: `Doctor appointment`
3. Save / Confirm the request so it is in the **To Approve** state (backend
   state `confirm`).

## Rules

- Exactly **one** time-off request for **June 15, 2026** must be created.
- **Half Day must be enabled**, with the **Morning** period (not afternoon).
- The duration must be **0.5 days** (half day).
- Do **not** request a whole day or an afternoon.
- Do **not** approve or refuse the request — leave it in the To Approve
  state.
