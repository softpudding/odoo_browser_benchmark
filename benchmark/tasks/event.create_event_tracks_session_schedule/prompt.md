# Build the conference session schedule

You are in the Odoo 19 **Events** app logged in as **Administrator**.

The event **Bench Tech Summit** on 2026-05-10 has been published but still has
no session schedule. The program committee needs two conference tracks on its
agenda so attendees can see the day's plan.

## What to do

1. Open the **Events** app and open the event **Bench Tech Summit**.
2. Click the **Tracks** smart button at the top of the event form to open the
   event's tracks list.
3. Create a **first** track with these exact values:
   - **Title**: `Bench Opening Keynote`
   - **Track Date**: `05/10/2026 09:00:00`
   - **Duration**: `1:00` (1 hour, so the stored float is `1.0`)
4. Save the track, then go back to the event's Tracks list.
5. Create a **second** track with these exact values:
   - **Title**: `Bench Closing Panel`
   - **Track Date**: `05/10/2026 16:00:00`
   - **Duration**: `1:30` (1 hour 30 minutes, so the stored float is `1.5`)
6. Save the second track.

## Rules

- Both tracks must be linked to the **Bench Tech Summit** event (same
  `event_id`).
- The titles must be EXACTLY `Bench Opening Keynote` and `Bench Closing Panel`
  (no trailing whitespace, no extra text).
- The dates must be entered in the Track Date field as shown — the admin user
  is in UTC so `05/10/2026 09:00:00` saves as `2026-05-10 09:00:00` UTC and
  `05/10/2026 16:00:00` saves as `2026-05-10 16:00:00` UTC.
- The durations must be EXACTLY 1.0 and 1.5 hours respectively.
- Do **not** create, modify, or delete any other event, track, or registration.
- Do **not** unpublish the event.
