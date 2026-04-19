# Release the reserved raw materials on a confirmed manufacturing order

You are in the Odoo 19 **Manufacturing** app logged in as **Administrator**.

Manufacturing order **MO-BENCH-UNRES** is a **confirmed** manufacturing
order for **5** units of **Bench Unres Product**. Its Bill of Materials
consumes **1 Bench Unres Mat** per unit, and warehouse **WH/Stock** has
**10 Bench Unres Mat** on hand. Because the MO has already been
**reserved** (Odoo's `action_assign()` ran during confirmation), **5
Bench Unres Mat** are currently held aside ("reserved") for this MO —
another team now needs those components for a more urgent job.

Your job is to **release the reservation** on this MO (unreserve the raw
materials) without cancelling the MO, without starting production, and
without touching the component quantities. The MO must stay **Confirmed**;
only its reservation state should change.

## What to do

1. Open the **Manufacturing** app and go to **Operations → Manufacturing
   Orders**. Clear any default search filters (Ready, To Do, etc.) so
   the confirmed MO is visible.
2. Open the manufacturing order **MO-BENCH-UNRES**.
3. In the form header (the status bar at the top of the form), locate
   the **Unreserve** button. It sits next to **Produce All**, **Check
   availability**, **Plan**, and **Cancel**. Click the **Unreserve**
   button.
4. That's it — no wizard, no dialog, no confirmation modal. The button
   disappears from the header (because the MO is no longer reserved)
   and the page stays on the MO form.

After you finish:

- The manufacturing order must still be named **MO-BENCH-UNRES** and its
  state must still be **Confirmed** (not Done, not Cancelled).
- The raw-material stock move for **Bench Unres Mat** must have its
  state changed from **Available / Assigned** back to **Confirmed** —
  i.e. the reservation has been released.
- The warehouse **WH/Stock** must still hold **10** Bench Unres Mat on
  hand, with **0** reserved for this MO (the 5 that were reserved are
  now free again).

## Rules

- Do **not** click **Cancel** — cancelling the MO is not unreserving
  it, and the task will fail.
- Do **not** click **Produce**, **Produce All**, or **Mark as Done** —
  the MO must stay **Confirmed**, not Done.
- Do **not** click **Check availability** — that would re-reserve the
  component after you unreserved it.
- Do **not** edit the Components tab, the BoM, or the on-hand stock.
- Do **not** change the MO's quantity, product, or BoM.
