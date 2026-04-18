# Buy one Standard and one VIP ticket for Bench Expo 2026

You are logged in to Odoo 19 as **Administrator**. A published event
named **`Bench Expo 2026`** has been seeded with **two** ticket types:

- **`Standard`** — price `50.00`
- **`VIP`** — price `150.00`

Your job is to go through the **public website registration + checkout
flow** to buy **one** Standard ticket and **one** VIP ticket, filling in
distinct attendee details for each, and pay via **Wire Transfer**.

## Step 1 — Open the public event page

1. Navigate to the public events listing at `/event` (singular; the URL
   `/events` also works).
2. Click the **Bench Expo 2026** card / title to open the event page.

## Step 2 — Select one Standard + one VIP ticket

1. Click the **Register** button on the event page. A **Tickets** modal
   opens listing both ticket types with a counter for each.
2. In the **Standard** ticket row, click the **`+`** button once to set
   its counter to `1`.
3. In the **VIP** ticket row, click the **`+`** button once to set its
   counter to `1`.
4. Verify both counters read `1` and then click the **Register** button
   at the bottom of the modal to continue.

## Step 3 — Fill the two attendee rows

An **Attendees** modal appears with **two** numbered sections — one per
ticket. Fill them as follows (the order depends on how the tickets are
listed; match by the ticket name shown above each section):

- **Ticket #… — Standard** section:
  - **Name**: `Alice Standard`
  - **Email**: `alice@benchexpo.test`
- **Ticket #… — VIP** section:
  - **Name**: `Bob VIP`
  - **Email**: `bob@benchexpo.test`

Phone fields are optional — leave them blank (or any value is
acceptable). Click **Go to Payment** at the bottom to submit.

## Step 4 — Checkout

Because the tickets are paid, submitting the Attendees form sends you
to the website checkout. If an **Address** / shipping page appears,
just click **Confirm** / **Next** to keep the admin's seeded address.

## Step 5 — Choose Wire Transfer and pay

You land on the **Payment** page (`/shop/payment`). Only one payment
option is listed: **Wire Transfer**.

1. Click the **Wire Transfer** option / radio to select it.
2. Click the **Pay now** button (you may have to accept any Terms &
   Conditions checkbox first).
3. You land on an **Order Confirmation** / **Wire transfer**
   instructions page. The quotation is now marked as sent (state
   `sent`, awaiting wire-transfer receipt) and both event
   registrations are linked to it. The task is complete — you do
   NOT need to go back to the back-office to confirm the payment.

## Final state to achieve

- Exactly **one** `sale.order` with state `sent` (or `sale`), containing
  **two** order lines:
  - one line for the `Bench Expo Standard Pass` product at price
    `50.00`, quantity `1`, linked to the Standard ticket,
  - one line for the `Bench Expo VIP Pass` product at price `150.00`,
    quantity `1`, linked to the VIP ticket.
  SO `amount_total` = `200.00`.
- Exactly **two** `event.registration` records on **Bench Expo 2026**,
  both linked to the same sale order:
  - `Alice Standard` / `alice@benchexpo.test` on the Standard ticket,
  - `Bob VIP` / `bob@benchexpo.test` on the VIP ticket.
- A Wire Transfer payment transaction in state `pending` for the sale
  order.

## Rules

- Do **not** create any additional registrations or extra sale orders.
- Do **not** change ticket prices or the event name/dates.
- Attendee names and emails must match the values above **exactly**
  (case-sensitive).
- Do **not** use the back-office (`/odoo/...`) to create the
  registrations or the sale order — go through the public website
  flow (`/event`, `/shop/checkout`, `/shop/payment`).
- Do **not** cancel the order after confirming payment.
