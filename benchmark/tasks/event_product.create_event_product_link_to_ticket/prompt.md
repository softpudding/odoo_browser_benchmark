# Create an event ticket product and link it on a new event ticket

You are in Odoo 19 logged in as **Administrator**. The Events team has
seeded an upcoming conference named **Spring Summit** but has not yet
created the service product that will be billed when attendees register.

Your job has two parts:

1. **Create the product** that will be used as the ticket product.
2. **Add a ticket type** on the event that uses that product.

## Step 1 — Create the product

1. Open the **Inventory** app (or Sales — either app exposes the Products
   menu).
2. Go to **Products → Products** and click **New**.
3. Fill in the product form:
   - **Product Name**: `Conference Pass Std`
   - **Product Type**: `Service`
   - **Sales Price**: `100.00`
4. On the **General Information** (or **Sales**) tab, set the
   **Service Tracking** field to **`Event Registration`**. This is the
   selection that allows the product to be picked as an event ticket
   product. (In Odoo 19 this option is added by the `event_product`
   bridge module — without it, the product will not show up in the
   event ticket product dropdown.)
5. **Save** the product.

## Step 2 — Add the ticket on the event

1. Open the **Events** app.
2. Open the event named **`Spring Summit`** (use the search bar if it
   is not on the first kanban page).
3. Click the **Tickets** tab.
4. Click **Add a line** and fill in the new ticket row:
   - **Product**: `Conference Pass Std` (pick the product you just
     created — do **not** create a new product from this dropdown)
   - **Name**: `Standard Pass`
   - **Price**: `100`
   - **Maximum** (Seats Max): `200`
5. **Save** the event.

## Final state

- A `product.product` record named **`Conference Pass Std`** exists,
  with `type = 'service'`, `list_price = 100.00`, and
  `service_tracking = 'event'`.
- The **Spring Summit** event has a ticket called **`Standard Pass`**
  linked to that product, with `price = 100` and `seats_max = 200`.

## Rules

- Create exactly **one** product named `Conference Pass Std`.
- Create exactly **one** ticket called `Standard Pass` on Spring
  Summit (the auto-generated `Registration for Spring Summit` placeholder
  ticket may already exist — leave it alone).
- Do **NOT** rename, archive, or change the dates of the **Spring
  Summit** event.
- Do **NOT** create attendees, sales orders, or invoices.
- The product must be a **Service** (not Goods / Consumable / Combo).
- Do **NOT** change the price after saving the ticket.
