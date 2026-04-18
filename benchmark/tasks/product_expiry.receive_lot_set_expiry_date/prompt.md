# Receive a perishable lot and set expiration & removal dates

You are in the Odoo 19 **Inventory** app logged in as **Administrator**.

A vendor receipt for **10** units of **Bench Perishable** is ready for
processing. **Bench Perishable** is a **lot-tracked** product that uses
expiration dates. You must create the lot on the fly, then set explicit
**Expiration Date** and **Removal Date** values on the lot record before
validating the receipt.

## What to do

1. Open the **Inventory** app and click the **Receipts** kanban tile.
2. Find and open the receipt whose **Source Document** is
   `BENCH-PERISH-RCV-01`.
3. On the **Bench Perishable** move line, click the **Details** button
   (the horizontal-lines icon at the right of the line) to open the
   Detailed Operations popup.
4. Inside the popup, in the **Lot/Serial Number** column of the single
   move-line row, type `BP-LOT-001` and accept the autocomplete option
   **Create "BP-LOT-001"** so a new lot is created.
5. Click the **internal-link** arrow that appears next to the lot name
   (the small arrow-in-a-box icon on the `Lot/Serial Number` cell) to
   open the **BP-LOT-001** stock.lot form.
6. On the lot form, in the **Dates** group, set:
   - **Expiration**: today **+ 60 days** at 00:00:00
   - **Removal Date**: today **+ 55 days** at 00:00:00
   Use the date pickers for each; leave Alert / Best before alone.
7. Save the lot form (cloud / floppy save icon), then close the lot
   form to return to the Detailed Operations popup, and click **Save**
   on the popup to apply the move line.
8. Back on the receipt form, click **Validate** in the header.

After validation:

- The receipt state must be **Done**.
- A `stock.lot` named **BP-LOT-001** must exist for **Bench Perishable**.
- That lot must have an explicit **Expiration Date** ≈ today + 60 days
  and an explicit **Removal Date** ≈ today + 55 days.

## Rules

- The lot name must be exactly `BP-LOT-001`.
- The received quantity must be exactly **10** (already pre-filled).
- The expiration and removal dates must be set on the **stock.lot**
  form; leaving them at the product template's default (today + 30 from
  `expiration_time`) is a failure.
- Do **not** create a backorder. Do **not** cancel the receipt.
- Do **not** change the product or the demand quantity.
