# Transfer a lot-tracked product into stock

You are in the Odoo 19 **Inventory** app logged in as **Administrator**.

An incoming transfer for **50** units of **Lot Product A** is waiting
for processing. The product is **lot-tracked**, so you must record a
specific lot number AND set the done quantity before validating.

## What to do

1. From the Inventory dashboard, click the **Receipts** kanban tile.
2. In the list of receipts, find and open the transfer whose
   **Source Document** is `BENCH-TRANSFER-LOT-01`.
3. On the **Lot Product A** move line:
   - Set the **Quantity** (done quantity) to exactly `50`.
   - In the **Lot/Serial Number** field, type `LOT-2026-001`. When the
     autocomplete shows a **Create "LOT-2026-001"** option, pick it to
     create the lot on the fly. (If the column is hidden, open the
     **Details** button on the line or use the column chooser to reveal
     Lot/Serial Number.)
4. Click **Validate** in the form header.
5. Do **not** accept a backorder — if a backorder dialog appears,
   choose **No Backorder**.

After validation:

- The transfer should be in **Done** state.
- A lot named `LOT-2026-001` should exist for **Lot Product A**,
  holding **50** units in the warehouse stock location (`WH/Stock`).

## Rules

- The lot number must be exactly `LOT-2026-001` (uppercase, with dashes).
- The done quantity must be exactly **50**.
- Do **not** create a backorder.
- Do **not** cancel the transfer.
- Do **not** change the demand quantity on the move line.
- Do **not** modify or validate any other transfer.
