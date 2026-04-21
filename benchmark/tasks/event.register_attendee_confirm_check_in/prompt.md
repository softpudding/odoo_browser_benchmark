# Register an attendee and check them in

You are in the Odoo 19 **Events** app logged in as **Administrator**.

The event **Product Update Q2 — Partners Meetup** is running, and a
walk-in guest needs to be registered and checked in.

## What to do

1. Open the **Events** app and open the event
   **Product Update Q2 — Partners Meetup**.
2. Click the **Attendees** stat button (or go to **Attendees** from the
   event's smart buttons / menu) to view the list of registrations.
3. Click **New** to register a new attendee with:
   - **Name**: `Sofia Reyes`
   - **Email**: `sofia.reyes@partner.example`
   - **Phone**: `+44 20 7946 0312`
4. Save. The registration is in **Registered** state.
5. **Check in** the attendee: click the **Attended** / **Check in**
   statusbar button. The registration moves to **Attended** state
   (backend state `done`).

## Rules

- Register exactly **one** attendee named **Sofia Reyes**.
- The final state of Sofia's registration must be **Attended**
  (backend `done`).
- Do **not** register anyone else.
- Do **not** cancel the registration.
- The attendee must be linked to **Product Update Q2 — Partners
  Meetup** — not any other event.
