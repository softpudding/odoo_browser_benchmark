You are in the Odoo 19 **Manufacturing** app as **Administrator**.
A confirmed manufacturing order **MO-BENCH-VAL** for **1 unit** of
**Bench Assembly** is already seeded. The finished product's category
uses **automated (real-time) stock valuation**, and the two required
components (**Bench Component 1** and **Bench Component 2**) each have
a standard cost of **10.00** set. Components are already on-hand at
the main warehouse.

## What to do

1. Go to **Manufacturing -> Manufacturing Orders**, find and open the
   MO **MO-BENCH-VAL**.
2. Click **Produce All** (or **Mark as Done**) in the form header to
   close the MO in a single step. Accept the default on any
   confirmation / consumption dialog so the MO moves to the **Done**
   state with 1 unit produced.

Once the MO is in the **Done** state, Odoo will automatically stamp
the stock moves with their valuation:
- the finished `stock.move` (for Bench Assembly) becomes **incoming**
  (`is_in=True`) with a **positive** value equal to the summed
  component cost;
- each component `stock.move` (for Bench Component 1 / 2) becomes
  **outgoing** (`is_out=True`) with a positive consumption value.

## Rules

- Do **NOT** reduce the quantity to produce below 1.
- Do **NOT** modify, add or remove any BoM line or component line on
  the MO.
- Do **NOT** cancel, reset or unlink the manufacturing order.
- Do **NOT** create a backorder -- produce the full 1 unit in one go.
- You do **NOT** need to touch the Accounting app, the Inventory
  Valuation report, or any journal -- closing the MO is enough.
