# Run manual replenishment for Bench Replenish Item

You are in the Odoo 19 **Inventory** app, logged in as **Administrator**.

A reordering rule has been configured for the storable product
**`Bench Replenish Item`** (Min 5 / Max 20) at location `WH/Stock`. The
product's sole vendor is **`Bench Replenish Vendor`** at unit price
**$50.00**. The on-hand quantity is **0**, so the Replenishment dashboard
will propose a quantity to order (20 units).

Run the manual replenishment from the Replenishment dashboard so Odoo
auto-generates a draft Request for Quotation to `Bench Replenish Vendor`
for 20 units of `Bench Replenish Item`.

## What to do

1. Open the **Inventory** app.
2. From the top menu, go to **Operations > Replenishment**. This opens
   the Replenishment dashboard (a list of
   `stock.warehouse.orderpoint` rows needing action — the default
   filter is "To Reorder").
3. Locate the row for **`Bench Replenish Item`**. It should show
   `Bench Replenish Vendor` (or the vendor name via the Vendor column
   if optional), `On Hand = 0`, `Min = 5`, `Max = 20`, `To Order = 20`.
4. On that row, click the inline **Order** button (the small
   truck icon at the right-hand side of the row, tooltip "Order").
   Do NOT click **Automate** (the refresh icon, which sets the trigger
   to `auto` — we want `manual`). Do NOT click **Snooze**.
5. A green notification should appear indicating the replenishment
   order has been generated (it links to the new RFQ). You do NOT
   need to open or confirm the RFQ — leaving it in `draft` is fine.

## Expected end state

- Exactly one new `purchase.order` exists for vendor `Bench Replenish Vendor`.
- It has exactly one `purchase.order.line` for `Bench Replenish Item`
  with `product_qty = 20` and `price_unit = 50.00`.
- The PO may be either `state = 'draft'` (RFQ) or `state = 'purchase'`
  (if you happened to also confirm it) — both are accepted.
- The original `stock.warehouse.orderpoint` remains active with
  `product_min_qty = 5.0`, `product_max_qty = 20.0`, and
  `trigger = 'manual'` (unchanged).

## Rules

- Use **Operations > Replenishment** (the dashboard that lives at
  `/odoo/replenishment`), NOT **Operations > Reordering Rules** (which
  does not render the per-row Order button).
- Click the per-row **Order** button (truck icon) on the
  `Bench Replenish Item` row — NOT the top dropdown bulk **Order** menu.
- Do NOT click **Automate** / **Order To Max** / **Snooze**.
- Do NOT modify the reordering rule's Min, Max, Location, or Trigger.
- Do NOT edit or cancel the generated RFQ.
- Do NOT change the vendor or the unit price.
- Do NOT create any additional reordering rule or purchase order by hand.
