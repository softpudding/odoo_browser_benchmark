# Produce a partial MO quantity and create a backorder for the rest

You are in the Odoo 19 **Manufacturing** app logged in as **Administrator**.

Manufacturing order **MO-BENCH-PARTIAL** is a confirmed manufacturing
order for **10** units of **Bench Widget**. Its Bill of Materials
consumes **1 Bench Mat** per Bench Widget and there are **10 Bench Mat**
on hand at **WH/Stock**.

The shop floor has only finished **4** of the 10 widgets so far, and
you need to close the production run now so those 4 widgets are
registered as produced today. The remaining **6** units must stay as a
**pending backorder** so another team can finish them later — do NOT
cancel them, do NOT discard them, and do NOT produce more than 4 on
this first run.

## What to do

1. Open the **Manufacturing** app and go to **Operations → Manufacturing
   Orders**. Clear any default search filters (Ready, To Do, etc.) so
   the confirmed MO is visible.
2. Open the manufacturing order **MO-BENCH-PARTIAL**.
3. In the form, find the **Quantity** line at the top (it reads
   `10.00 / 10.00 Units  To Produce`). The left-hand number is the
   **Quantity Producing** for this run — **change it from 10 to 4**
   (click the left-hand `10.00`, clear it, type `4`, then Tab out of
   the field to commit the edit).
4. Click the **Produce** button in the form header. (Because
   `Quantity Producing < Quantity`, the header button is labeled
   **Produce**, not **Produce All**.)
5. A dialog titled **"You produced less than the initial demand"**
   (model `mrp.production.backorder`) will appear. It has two buttons:
   - **Create backorder** (primary, blue)
   - **No Backorder** (secondary)

   Click the primary **Create backorder** button. This closes the
   current run as 4 units produced and opens a sibling backorder
   manufacturing order for the remaining 6 units.
6. You'll be redirected to the new backorder MO form — you can leave
   that form as-is. Do NOT confirm, produce, or cancel the backorder.

After you finish:

- The original manufacturing order (Odoo will have renamed it from
  `MO-BENCH-PARTIAL` to `MO-BENCH-PARTIAL-001` when the backorder was
  split off) must be in **Done** state with **4 units produced**.
- A second `mrp.production` record named `MO-BENCH-PARTIAL-002` (the
  backorder) must exist with the remaining **6** units, linked to the
  same production group, in a non-done, non-cancelled state
  (**Confirmed** / **In Progress**).

## Rules

- Do **not** cancel **MO-BENCH-PARTIAL** or its backorder.
- Do **not** click **No Backorder** on the dialog — that would discard
  the remaining 6 units.
- Do **not** change the planned **Quantity** (the right-hand `10.00` of
  the original MO) — only the left-hand **Quantity Producing** goes
  from 10 to 4.
- Do **not** touch the Bill of Materials, the component list, or the
  on-hand stock.
- Do **not** produce and close the backorder — leave it pending.
