You are in the Odoo 19 **Manufacturing** app as **Administrator**.

A confirmed manufacturing order **MO-BENCH-WO** for **1 unit** of
**Bench Assembly Kit** is already seeded. The kit has one serial-tracked
component, **Bench Serial Part**, and a single work order **Final
Assembly** that runs on workcenter **WC-01**.

Four serial numbers of **Bench Serial Part** are available in stock:
**SN-A**, **SN-B**, **SN-C**, and **SN-D** (one unit each at WH/Stock).
Odoo may have auto-reserved one of them (typically **SN-A**) when the
manufacturing order was confirmed, but **that is NOT the serial you must
consume**.

## What to do

You must consume **SN-B** (not SN-A, not SN-C, not SN-D), finish the
work order, and close the manufacturing order. You can use either
the **Manufacturing** backend MO form OR the Shop Floor tablet UI —
either flow is acceptable as long as the end state is correct.

One straightforward path via the backend MO form:

1. Open the manufacturing order **MO-BENCH-WO** (Manufacturing ->
   Operations -> Manufacturing Orders).
2. Open the **Work Orders** tab and **Start** the **Final Assembly**
   work order (this moves the work order into the `In Progress` state
   and the MO into `In Progress`).
3. Go to the **Components** tab on the MO. The line for **Bench Serial
   Part** shows a **Details** button (the small list icon). Click it
   to open the Detailed Operations popup for that component.
4. In the Detailed Operations popup, set the **Lot/Serial** for the
   single line to **SN-B** (if there is a pre-populated line reserved
   for SN-A, change it to SN-B; if there is no line yet, add one with
   `Lot/Serial = SN-B`, `Quantity = 1`). Save the popup.
5. Back on the MO form, re-open the Work Orders tab and click **Done**
   on the **Final Assembly** work order (this finishes the work order;
   its state becomes `Finished`).
6. In the MO form header, click **Produce All** / **Mark as Done** so
   the MO itself moves to the **Done** state.

After you finish, the manufacturing order must be in the **Done**
state, the **Final Assembly** work order must be in the **Finished**
state, and **SN-B** must be the only serial that was consumed.

## Rules

- Do NOT cancel the MO or the work order.
- Do NOT consume **SN-A**, **SN-C**, or **SN-D** — only **SN-B**.
- Do NOT create a backorder — produce the full 1 unit in one go.
- Do NOT change the quantity to produce (leave it at 1).
- Do NOT modify the BoM, the product list, or the workcenter.
- Do NOT create any new serial numbers; use only the pre-seeded lots.
