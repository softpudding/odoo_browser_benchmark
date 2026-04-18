# Configure a paid ticket, register an attendee, and invoice them

You are in Odoo 19 logged in as **Administrator**. The events team has set
up the conference **Spring Dev Summit 2026** but it has no ticket types
yet. The seed has prepared a service product **Dev Summit Pro Product**
(list price 150) that will be used as the ticket product. The customer
**Bench Summit Attendee Inc** has been created in Contacts.

You need to:
1. Add a paid ticket type to the event,
2. Sell that ticket to **Bench Summit Attendee Inc** as a sales order,
3. Confirm the sale so the attendee registration is generated, fill in
   the attendee details (**Berta Attendee** / `berta@benchsummit.test`),
4. Generate a customer invoice from the sales order — leave it in
   **Draft** (do **NOT** post / confirm / validate it).

## Step 1 — Add the ticket on the event

1. Open the **Events** app.
2. Open the event named **`Spring Dev Summit 2026`**.
3. Click the **Tickets** tab.
4. Click **Add a line** and fill in the new ticket row:
   - **Product**: `Dev Summit Pro Product` (the service product the
     seed already created — pick it from the dropdown, do not create a
     new product)
   - **Name**: `Professional Pass`
   - **Price**: `150`
   - **Maximum** (seats max): `50`
5. **Save** the event.

## Step 2 — Create a sales order for one ticket

1. Open the **Sales** app.
2. Click **New** to create a new quotation.
3. Set the **Customer** to `Bench Summit Attendee Inc`.
4. In the **Order Lines** tab, click **Add a product** and pick
   `Dev Summit Pro Product`.
5. The **Configure an event** dialog opens. Set:
   - **Event**: `Spring Dev Summit 2026`
   - **Event Ticket**: `Professional Pass`
   Then click **Ok** to close the configurator.
6. Make sure the line **Quantity** is `1` and the **Unit Price** is
   `150.00`.
7. Click **Confirm** to confirm the sales order.

## Step 3 — Fill in the attendee details

When the sales order is confirmed, the **Event Registrations**
attendee-details dialog opens. In that dialog row:

- **Name**: `Berta Attendee`
- **Email**: `berta@benchsummit.test`

Then click **Create/Update registrations** to close the dialog. The
event registration is now in the **Registered** state (`open`).

## Step 4 — Generate the customer invoice (draft only)

Back on the confirmed sales order:

1. Click the **Create Invoice** button at the top.
2. The **Create invoices** wizard opens. Keep the default
   **Regular invoice** option (do **NOT** pick a down payment option).
3. Click **Create Draft Invoice** in the wizard footer.

The wizard creates a customer invoice in the **Draft** state and
navigates you to it. **Stop here.** Do not confirm, post, validate or
register payment on this invoice.

## Final state

- One **Professional Pass** ticket on **Spring Dev Summit 2026**, price
  `150`, max seats `50`, linked to the **Dev Summit Pro Product** product.
- One **sale.order** for **Bench Summit Attendee Inc** in **Sales Order**
  state (`sale`), one order line with quantity `1` for the ticket
  product at `150.00`.
- One **event.registration** for **Berta Attendee**
  (`berta@benchsummit.test`) on **Spring Dev Summit 2026** in the
  **Registered** state (`open`), linked to the Professional Pass
  ticket.
- One **customer invoice** (`account.move`, `move_type =
  out_invoice`) for **Bench Summit Attendee Inc** in **Draft** state
  (`draft`) with total `150.00`.

## Rules

- Use the seeded **Dev Summit Pro Product**; do not create a new
  product. Do not change its price.
- Create exactly **one** ticket type, **one** sales order, **one**
  registration, **one** invoice.
- Do **NOT** post, confirm, validate, send, or register payment on the
  invoice — it must remain in **Draft**.
- Do **NOT** check in, attend, or cancel the registration.
- Do **NOT** modify or rename **Spring Dev Summit 2026** itself
  (keep the event name and dates as seeded).
