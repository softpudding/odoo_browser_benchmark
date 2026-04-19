# Deliver partial shipment and decline the backorder

You are in the Odoo 19 **Inventory** app, logged in as **Administrator**.

The warehouse must ship a delivery for customer **Bench Ship Co**. Our picker
only loaded **3** units of `Bench Pick Item` onto the truck even though the
order demands **5**. The sales team has already told the customer that the
missing **2** units will **NOT** be shipped later — they're writing it off, so
no backorder should be created.

## Background state

A **Ready** (reserved / assigned) outgoing delivery picking already exists:

- **Reference / Name**: `WH/OUT/BENCH-BACKORDER-NO`
- **Customer (Delivery Address)**: `Bench Ship Co`
- **Operation Type**: `Delivery Orders` (outgoing)
- **Single move line**: `Bench Pick Item`, Demand **5**, Quantity (Done) **5** (fully reserved)
- On-hand at `WH/Stock`: **5** units of Bench Pick Item

You do NOT need to click Check Availability — the picking is already reserved.

## What to do

1. Open the **Inventory** app and navigate to the **Delivery Orders** transfers
   list (click the Delivery Orders kanban tile on the Inventory overview, or
   use Operations > Transfers filtered to Delivery Orders).
2. Open the delivery whose reference is `WH/OUT/BENCH-BACKORDER-NO`.
3. On the single `Bench Pick Item` row in the **Operations** tab, click the
   inline **Quantity** cell (the Done qty, currently showing `5.00`) and change
   the value from **5** to **3**. Press Tab (or click outside the cell) so the
   edit commits.
4. In the header, click **Validate**.
5. A **Create Backorder?** dialog appears (because Quantity `3` is less than
   Demand `5`). The dialog has two buttons:

   - **Create Backorder** — primary / highlighted / left button (this is the
     DEFAULT — DO NOT click it)
   - **No Backorder** — secondary / right button (CLICK THIS ONE)

   Click the **No Backorder** button. The missing 2 units will be dropped, no
   backorder picking will be created.
6. The picking state should become **Done**.

## Rules

- The original picking `WH/OUT/BENCH-BACKORDER-NO` MUST end in state **Done**
  with the single Bench Pick Item move reporting Quantity (Done) = **3**.
- **NO backorder** `stock.picking` may exist — after Validate, there must be
  zero pickings whose `backorder_id` equals the original's id.
- You MUST click the secondary **No Backorder** button in the dialog. Do NOT
  click **Create Backorder** (that is the default/primary button and creates
  the unwanted backorder).
- Do NOT change the Demand value. Only edit the Quantity (Done) cell.
- Do NOT cancel or unlink the original picking.
- Do NOT add extra products, extra lines, or extra pickings.
