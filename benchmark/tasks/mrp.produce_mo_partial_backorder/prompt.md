# Partially produce a manufacturing order and create a backorder

You are in the Odoo 19 **Manufacturing** app logged in as **Administrator**.

A confirmed manufacturing order **WH/MO/BENCH-PART-001** is planned for
**10** units of **Bench Chassis Z**, but the factory only finished
**6** units today. The remaining **4** units must stay planned as a
backorder.

## What to do

1. Open the **Manufacturing** app and go to **Operations → Manufacturing
   Orders**.
2. Open the manufacturing order **WH/MO/BENCH-PART-001**.
3. On the form, change **Quantity Producing** (the editable quantity
   field near the top, sometimes labeled "Quantity") from **10** to
   **6**.
4. Click **Produce** in the form header (the button label reflects the
   partial quantity).
5. A dialog will appear asking what to do with the remaining quantity.
   Select **Create Backorder** so the remaining 4 units are kept as a
   new manufacturing order.

After you finish, two manufacturing orders should exist:

- The produced MO (typically renamed to **WH/MO/BENCH-PART-001-001**)
  in **Done** state with **6** units produced.
- The backorder MO (typically **WH/MO/BENCH-PART-001-002**) for the
  remaining **4** units, still in a confirmed / planned state with 0
  units produced.

## Rules

- Do **not** cancel the manufacturing order.
- Do **not** choose "No Backorder" — the remaining 4 units must be
  preserved in a new backorder MO.
- Do **not** modify the Bill of Materials, the component lines, or the
  finished product.
- Do **not** create any extra manufacturing orders beyond the automatic
  backorder.
