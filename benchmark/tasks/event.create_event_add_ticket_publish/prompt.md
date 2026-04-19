# Create an event, add a paid ticket, and publish it

You are in Odoo 19 logged in as **Administrator**. The events team needs
a new conference registered in the system with one paid ticket type, and
the event must be visible on the public website.

## Step 1 — Create the event

1. Open the **Events** app (it is already open at the list of events).
2. Click **New** to create a new event.
3. Set the **Event Name** to exactly `Bench Summer Summit 2026`.
4. Set the **Date** range so the event runs from
   **June 15, 2026 09:00:00** to **June 15, 2026 17:00:00** (local time).
5. Save the event (click the cloud/save icon or press the save shortcut).

## Step 2 — Add a paid ticket type

1. Open the **Tickets** tab on the event form.
2. Click **Add a line** and add a single ticket:
   - **Name**: `General Admission`
   - **Price**: `50`
3. Leave the seat limit OFF (do NOT enable the seat limit on this ticket).
4. Save the event again so the ticket persists.

## Step 3 — Publish the event on the website

- With the event record still open, flip the **Published** toggle at the
  top right of the form (the small switch next to the "Go to Website"
  button in the breadcrumb/header area). The toggle should end up in the
  **Published** (green/on) state.
- Save the record if the form is still in edit mode.

## Final state

- Exactly **one** `event.event` record named `Bench Summer Summit 2026`
  with `date_begin` = **2026-06-15 09:00:00** (local) and
  `date_end` = **2026-06-15 17:00:00** (local).
- Exactly **one** `event.event.ticket` on that event named
  `General Admission` with a unit price of **50.00**.
- The event's `is_published` flag is **True**.

## Rules

- Create exactly **one** event and exactly **one** ticket type. Do not
  leave phantom empty ticket rows behind.
- The event name must be exactly `Bench Summer Summit 2026` — no extra
  whitespace, no different capitalization.
- The ticket name must be exactly `General Admission`.
- Do **NOT** delete or archive the event once created.
- Do **NOT** create extra tickets (no VIP, no Early Bird, no
  auto-suggested "Registration" rows left over from a draft save).
- Do **NOT** modify any other events in the database.
