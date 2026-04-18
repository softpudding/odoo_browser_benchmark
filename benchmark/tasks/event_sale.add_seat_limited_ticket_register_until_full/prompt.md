# Add a 5-seat VIP ticket and register attendees until the seats fill

You are in Odoo 19 logged in as **Administrator**. The Events team has
seeded a workshop named **Spring Q2 Workshop** but it has no ticket
types yet. Your job is to add a strictly limited VIP ticket and then
fill it up one attendee at a time, observing that Odoo blocks the
sixth registration.

## Step 1 — Add the VIP ticket on the event

1. Open the **Events** app.
2. Open the event named **`Spring Q2 Workshop`** (use the search bar
   if it is not visible — it has no tickets yet).
3. Click the **Tickets** tab.
4. Click **Add a line** and fill in the new ticket row:
   - **Name**: `VIP Seat`
   - **Price**: `200`
   - **Maximum** (Seats Max): `5`
5. **Save** the event.

## Step 2 — Register five attendees on the VIP Seat ticket

For **each** of the five attendees below, do this loop:

1. Click the **Attendees** smart-button on the event form (or use the
   Attendees menu) to open the registrations list.
2. Click **New** to create a new registration.
3. Set **Event Ticket** to `VIP Seat` (the field may be blank by
   default — pick `VIP Seat` from the dropdown).
4. Set the attendee **Name** to the value from the table below.
5. **Save** the registration. The state should become **Registered**.
6. Go back to the event (breadcrumb) and repeat for the next attendee.

| # | Name   |
|---|--------|
| 1 | `VIP-1` |
| 2 | `VIP-2` |
| 3 | `VIP-3` |
| 4 | `VIP-4` |
| 5 | `VIP-5` |

After saving the fifth registration, the **VIP Seat** ticket is full
(0 available seats).

## Step 3 — Attempt a sixth registration and confirm Odoo blocks it

1. From the event's Attendees list, click **New** again.
2. Set **Event Ticket** to `VIP Seat`.
3. Set the attendee **Name** to `VIP-6`.
4. Try to **Save**. Odoo must refuse to save the record because the
   ticket is sold out — you will see an error/warning dialog of the
   form *"There are not enough seats available for Spring Q2
   Workshop"*.
5. **Discard** that draft (do **not** force-save it; do **not** raise
   the seat limit; do **not** create the registration on a different
   ticket).

## Final state

- One **VIP Seat** ticket on **Spring Q2 Workshop**, price `200`,
  seats max `5`.
- **Exactly 5** event.registration records on **Spring Q2 Workshop**,
  named **VIP-1, VIP-2, VIP-3, VIP-4, VIP-5**, all linked to the
  **VIP Seat** ticket and all in **Registered** state.
- **No** registration named **VIP-6** anywhere in the database.
- The event itself is unchanged (same name, same dates).

## Rules

- Create exactly **one** ticket type on the event (`VIP Seat`).
- Do **NOT** raise `Seats Max` above 5 to force VIP-6 in.
- Do **NOT** create the sixth attendee under a different ticket or
  on a different event.
- Do **NOT** cancel, archive or check in any of the five Registered
  attendees.
- Do **NOT** rename the event or change its dates.
