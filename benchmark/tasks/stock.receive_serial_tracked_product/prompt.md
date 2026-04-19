# Receive a serial-tracked product with three exact serial numbers

You are in the Odoo 19 **Inventory** app logged in as **Administrator**.

A vendor receipt for **3** units of **Bench Serial Gadget** is ready
for processing. This product is **serial-tracked**, so you must record
an individual **serial number** for every single unit before validating
the receipt.

## What to do

1. Open the **Inventory** app and click the **Receipts** kanban tile.
2. Find and open the receipt whose **Source Document** is
   `BENCH-SN-RCV-01`. Its source is the **Vendors** location and its
   destination is **WH/Stock**, with one line for `Bench Serial Gadget`
   demand = `3`.
3. Confirm the receipt if it is still in draft (click **Mark as Todo**
   or **Confirm** in the header so the move becomes ready).
4. Open **Detailed Operations** on the `Bench Serial Gadget` move line
   (click the **Details** / operations icon on the line, or expand the
   line into the detailed operations popup).
5. In the popup, make sure there are **exactly three** move-line rows —
   one for each unit — and fill them in as follows:

   | Lot/Serial Number | Quantity |
   |-------------------|----------|
   | `SN-BENCH-001`    | `1`      |
   | `SN-BENCH-002`    | `1`      |
   | `SN-BENCH-003`    | `1`      |

   For each serial number, when the autocomplete shows a
   **Create "SN-BENCH-xxx"** option, select it so the serial is
   created on the fly. Do not reuse an existing serial.
6. **Save / close** the Detailed Operations popup.
7. Click **Validate** in the form header.

After validation:

- The receipt should be in **Done** state.
- Three `stock.lot` records with names `SN-BENCH-001`, `SN-BENCH-002`,
  and `SN-BENCH-003` should exist for `Bench Serial Gadget`.
- Each serial should end up at **WH/Stock** with quantity 1.

## Rules

- The three serial numbers must be **exactly** `SN-BENCH-001`,
  `SN-BENCH-002`, and `SN-BENCH-003` (uppercase, with dashes).
- There must be **exactly three** move-line rows on the receipt, each
  with quantity **1** and a distinct serial.
- Do **not** enter all three serials into a single line.
- Do **not** create a backorder — receive the full quantity.
- Do **not** cancel or unlink the receipt.
- Do **not** change the demand quantity (it is already 3).
