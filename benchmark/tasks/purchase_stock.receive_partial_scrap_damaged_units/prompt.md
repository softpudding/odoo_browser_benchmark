# Receive partial PO, scrap 5 damaged units to WH/Lost, backorder the rest

You are in the Odoo 19 **Purchase** app, logged in as **Administrator**.

The receiving crew reports that our vendor **Bench Parts Vendor** delivered
only 15 of the 20 **Bench Parts** units we ordered on purchase order
`P-BENCH-DMG-001`, and **5 of those 15 arrived damaged**. You must:

- Mark the good units as received (Done = 15).
- Scrap the 5 damaged units to the dedicated **WH/Lost** inventory location.
- Validate the transfer and create a **backorder** for the 5 units still owed
  by the vendor.

## Background state

A confirmed purchase order is waiting:

- **PO Reference / Source Document**: `P-BENCH-DMG-001`
- **Vendor**: `Bench Parts Vendor`
- **Order line**: `Bench Parts`, quantity **20**

Its associated receipt is already **Ready** (assigned) — you do not need to
create a new transfer.

## What to do

### Part A — Open the receipt

1. From the Purchase app, open PO `P-BENCH-DMG-001`.
2. Click the **Receipt** smart button in the header to open the associated
   vendor receipt (it is in the **Ready** state).

### Part B — Record only the good units (Done = 15)

3. On the receipt's **Operations** tab, locate the `Bench Parts` line.
4. In the **Quantity** (Done) cell of that line, change the value to **15**
   (the cell might default to 20 because the transfer auto-reserved the full
   demand — you MUST lower it to 15).
5. Let the form auto-save after the edit (click elsewhere on the form or
   press Tab to commit).

### Part C — Scrap the 5 damaged units to WH/Lost

6. On the same receipt, open the **cog / Actions** menu at the top of the
   form (next to the breadcrumb; it may be labelled `Actions` or rendered
   as the gear / cog icon) and click **Scrap**.
7. The **Scrap Products** dialog appears. Fill it in exactly:
   - **Product**: `Bench Parts`
   - **Quantity**: change `1.00` to **5** (the default is 1.00; you MUST
     overwrite it to 5).
   - **Scrap Location**: change the default to **WH/Lost** (type `WH/Lost`
     in the Scrap Location field and pick the matching entry; do NOT
     leave the default `Virtual Locations/Scrap`).
8. Click **Scrap Products** in the dialog footer to validate the scrap. The
   dialog closes and you return to the picking form.

### Part D — Validate the picking and create a backorder

9. On the picking form header, click **Validate**.
10. A **Create Backorder?** dialog appears asking how to handle the 5 units
    still owed. Click **Create Backorder** (the left-hand primary action) —
    do NOT click **No Backorder**.
11. The picking state becomes **Done**. A fresh backorder picking is created
    automatically for the remaining 5 units and appears under the PO's
    Receipt smart button count (now 2 receipts: the original Done one and
    the new Ready backorder).

## Rules

- The original receipt MUST end in state **Done** with the Bench Parts
  move line reporting **quantity = 15** (the "Done" amount that was
  actually received).
- Exactly **one** `stock.scrap` record must exist for this PO's flow,
  carrying product `Bench Parts`, `scrap_qty = 5`, and
  `scrap_location_id = WH/Lost`. Do NOT leave the scrap_qty at the
  default `1.00`, and do NOT scrap to `Virtual Locations/Scrap`.
- A **backorder** `stock.picking` MUST exist with the same vendor and 5
  units of Bench Parts still to receive (state in `assigned` / `ready`
  / `confirmed`).
- Do NOT cancel or unlink the original receipt or the PO.
- Do NOT create any extra scrap records, extra PO lines, or extra
  products.
