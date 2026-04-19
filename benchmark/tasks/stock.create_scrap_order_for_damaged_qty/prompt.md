# Scrap 3 damaged units of Bench Scrap Item from WH/Stock

You are in the Odoo 19 **Inventory** app, logged in as **Administrator**.

The warehouse has **10** units of the storable product **`Bench Scrap Item`**
on hand in `WH/Stock`. Three of them arrived damaged and must be written off
through a scrap order.

## What to do

1. In the Inventory app, open the top menu **Operations > Scrap** to reach
   the **Scrap Orders** list view.
2. Click **New** to start a fresh scrap record.
3. In the scrap form:
   - Set **Product** to `Bench Scrap Item`.
   - Set **Quantity** to `3` (overwrite the default `1.00`).
   - Leave **Source Location** at the default `WH/Stock`.
   - Leave **Scrap Location** at its default (`Virtual Locations/Scrap`).
4. Save the record (cloud/floppy icon) so the scrap is created in state
   `draft`.
5. Click the **Validate** button in the form header — this moves the 3 units
   from `WH/Stock` to `Virtual Locations/Scrap` and flips the scrap state to
   `Done`.

## Rules

- The new `stock.scrap` MUST have `product_id = Bench Scrap Item`,
  `scrap_qty = 3`, and end in state **Done**.
- The scrap must come from `WH/Stock`; do NOT change the Source Location to
  a different warehouse or virtual location.
- Do NOT edit the product's on-hand quantity directly via inventory
  adjustment — use the Scrap flow.
- Do NOT create more than one scrap order.
- Do NOT cancel or delete the scrap after validating it.
- Do NOT change `Bench Scrap Item` itself (name, type, routes).
