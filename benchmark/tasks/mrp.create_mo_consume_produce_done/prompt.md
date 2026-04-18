# Create a manufacturing order from scratch, consume components, and close it

You are in the Odoo 19 **Manufacturing** app logged in as **Administrator**.

A Bill of Materials for product **Bench Assembly** already exists. It
consumes **1 Bench Part A** and **2 Bench Part B** per finished unit.
There is **no manufacturing order yet** — you must create one from
scratch and run it through to completion.

## What to do

1. Open the **Manufacturing** app and go to **Operations → Manufacturing
   Orders**.
2. Click **New** to create a new manufacturing order.
3. Fill in the form:
   - **Product**: `Bench Assembly`
   - **Quantity**: `3`
   Leave other fields at their defaults. The Bill of Materials for
   Bench Assembly is auto-selected and the component lines (Bench Part
   A qty 3, Bench Part B qty 6) appear after you select the product and
   quantity.
4. Click **Confirm** in the status bar. The MO moves from **Draft** to
   **Confirmed** and raw-material moves are created.
5. Click **Produce All** (also labeled **Mark as Done**) to finish the
   manufacturing order. If a consumption / consumption-warning dialog
   appears asking whether to **Apply** / **Continue** / **Validate**,
   accept it so the MO transitions to **Done** with the full 3 units
   produced.
6. Make sure the final MO state is **Done** with **Quantity Produced =
   3**.

After you finish:

- Exactly **one** `mrp.production` record exists for **Bench Assembly**
  with **Quantity = 3**, state **Done**, and quantity produced **3**.
- The MO consumed **3 Bench Part A** and **6 Bench Part B** (those are
  the `stock.move` raw-material lines).
- A finished `stock.move` produced **3 Bench Assembly**.

## Rules

- Do **not** cancel, unlock, or delete the MO once you create it.
- Do **not** change the Bill of Materials or its component quantities.
- Do **not** create additional manufacturing orders, unbuild orders, or
  scrap orders — create **one** MO only.
- The finished product is **Bench Assembly** (not Bench Part A or
  Bench Part B). Do not pick a component product by mistake.
- Do **not** change the planned quantity after confirming. The MO must
  close at **3 units produced**.
