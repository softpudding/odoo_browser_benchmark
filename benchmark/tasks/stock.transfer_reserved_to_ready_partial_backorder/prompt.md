# Deliver a partial shipment and create a backorder via Detailed Operations

You are in the Odoo 19 **Inventory** app, logged in as **Administrator**.

The warehouse is ready to dispatch a delivery for customer **Bench Partial Cust**,
reference `D-BENCH-PARTIAL-001`. We have **10** units of `Bench Partial Item` on
hand in `WH/Stock`, but the driver can only take **7** today. You must reserve
the full demand, ship 7 now, and let Odoo create a backorder for the remaining 3.

## Background state

An outgoing **Confirmed** (Waiting) delivery picking already exists:

- **Reference / Source Document**: `D-BENCH-PARTIAL-001`
- **Customer (Delivery Address)**: `Bench Partial Cust`
- **Operation Type**: `Delivery Orders` (outgoing)
- **Single move line**: `Bench Partial Item`, demand **10**
- On-hand in `WH/Stock`: **10** units of Bench Partial Item

The picking has not yet been reserved. You must drive reservation, then ship 7.

## What to do

### Part A — Open the picking and reserve stock

1. Open the **Inventory** app and navigate to the **Delivery Orders** transfers
   list (click the Delivery Orders kanban tile on the overview, or Operations >
   Transfers filtered to Delivery Orders).
2. Open the delivery with source document `D-BENCH-PARTIAL-001`.
3. In the form header, click **Check Availability**. The picking's single move
   line should become reserved with **Quantity = 10** (picking state becomes
   **Ready / Assigned**).

### Part B — Open Detailed Operations and edit to 7

4. On the `Bench Partial Item` move line in the **Operations** tab, click the
   **Details** button (the small icon/button at the right edge of the move row)
   to open the **Detailed Operations** popup (a modal showing `stock.move.line`
   rows with columns `From`, `To`, `Lot/Serial Number`, `Quantity`, ...).
5. In the popup there is exactly one move-line row (the one reserved by Check
   Availability). Click the **Quantity** cell on that row and change the value
   from **10** to **7**.
6. Click **Save** in the popup footer (or the floppy-disk save icon) to save
   and close the popup. The picking form should now show Quantity **7** on the
   move line (still with demand 10).

### Part C — Validate and create a backorder

7. Back on the picking form, click **Validate** in the header.
8. The **Create Backorder?** dialog appears because Quantity (7) is less than
   Demand (10). Click **Create Backorder** — this is the **left-hand primary
   action** on the dialog footer. Do NOT click **No Backorder**.
9. The picking state becomes **Done**. A new backorder `stock.picking` is
   created automatically for the remaining 3 units (state **Ready /
   Assigned**) — you do NOT need to open or validate the backorder.

## Rules

- The original picking `D-BENCH-PARTIAL-001` MUST end in state **Done** with
  the single Bench Partial Item move reporting **quantity = 7**.
- A **backorder** `stock.picking` MUST exist with `backorder_id == original.id`,
  one Bench Partial Item move, **product_uom_qty = 3**, state in
  `assigned` / `confirmed` — do NOT validate or cancel the backorder.
- You MUST click **Check Availability** on the original picking before editing
  the quantity — without reservation, validating the picking raises an
  "Immediate Transfer?" / availability wizard instead of the Create Backorder
  dialog.
- You MUST edit the quantity via the **Detailed Operations** popup (click
  Details, change Quantity, Save). Editing the inline "Quantity" cell directly
  in the picking-form list often does not persist in Odoo 19.
- Do NOT change the demand (`Demand` column) — only the Quantity (Done) value.
- Do NOT unreserve, cancel, or unlink the original picking or the backorder.
- Do NOT add extra products, extra lines, or extra pickings.
