# Sell an event ticket product and fill in the attendee details

You are in Odoo 19 logged in as **Administrator**. The events team has already
created the conference **Bench Summit** with a single paid ticket type
**Standard Pass** (price 100) linked to the service product
**Bench Summit Ticket** (Service Tracking = *Event Registration*). The
customer **Bench Attendee Co** also already exists in Contacts.

You need to sell one **Standard Pass** ticket to that customer, record the
attendee's personal details on the generated registration, and confirm the
sale. Start from the **Sales** app.

## Step 1 — Create the sales order

1. Open the **Sales** app.
2. Click **New** to create a new quotation.
3. Set the **Customer** to `Bench Attendee Co`.
4. In the **Order Lines** tab, click **Add a product** and pick
   `Bench Summit Ticket` from the product dropdown.
5. Because this product tracks by event, the **Configure an event** dialog
   opens automatically. In that dialog:
   - **Event**: `Bench Summit`
   - **Event Ticket**: `Standard Pass`
   Then click **Ok** to close the configurator.
6. Make sure the line **Quantity** is `1` (the default) and the **Unit Price**
   is `100.00`.

## Step 2 — Confirm the sale and fill attendee details

1. Click **Confirm** in the sales order header to confirm the quotation.
2. The **Event Registrations** attendee-details dialog opens for the newly
   created registration. In that single row, set:
   - **Name**: `Alice Attendee`
   - **Email**: `alice@bench.test`
3. Click **Create/Update registrations** (the primary button in the dialog
   footer) to save the attendee details and close the dialog.

## Final state

- One **sale.order** for **Bench Attendee Co** in the **Sales Order** state
  (`sale`), with one line for `Bench Summit Ticket`, quantity `1`, unit price
  `100.00`, linked to the **Standard Pass** ticket on **Bench Summit**.
- One **event.registration** on **Bench Summit**:
  - **Name**: `Alice Attendee`
  - **Email**: `alice@bench.test`
  - **Ticket**: `Standard Pass`
  - State: **Registered** (`open`)
  - Linked to the confirmed sales order line.

## Rules

- Use the seeded **Bench Summit Ticket** product; do NOT create a new
  product.
- Use the seeded **Standard Pass** ticket on **Bench Summit**; do NOT add
  another ticket type.
- Create exactly **one** sales order and **one** registration.
- The attendee **Name** must be `Alice Attendee` and the **Email** must be
  `alice@bench.test` — do NOT leave them at the Administrator defaults.
- Do NOT generate an invoice, do NOT post anything else, and do NOT cancel
  or check-in the registration.
- Do NOT rename or modify the event itself (keep `Bench Summit` and its
  dates as seeded).
