# Receive a lot-tracked product with an exact lot number

You are in the Odoo 19 **Inventory** app logged in as **Administrator**.

A vendor receipt for **20** units of **Apex Turbine Rotor** is ready
for processing. This product is **lot-tracked**, so you must record
the **lot number** before validating the receipt.

## What to do

1. Open the **Inventory** app and click the **Receipts** kanban tile.
2. Find and open the receipt whose **Source Document** is
   `BENCH-LOT-RCV-01`.
3. The Quantity column is already filled with **20** for you. On
   the Apex Turbine Rotor move line, find the **Lot/Serial Number**
   column (it may be hidden — use the column chooser / "Optional
   columns" toggle if needed to reveal it) and type the lot number
   `LOT-2026-R042`. When the autocomplete shows a **Create
   "LOT-2026-R042"** option, select it to create the lot on the fly.
4. Click **Validate** in the form header.

After validation:

- The receipt should be in **Done** state.
- A lot with name `LOT-2026-R042` should exist for the Apex Turbine
  Rotor product, holding **20** units in the warehouse stock location.

## Rules

- The lot number must be exactly `LOT-2026-R042`.
- The done quantity must be exactly **20**.
- Do **not** create a backorder — receive the full quantity.
- Do **not** cancel the receipt.
- Do **not** modify the demand quantity on the move line.
